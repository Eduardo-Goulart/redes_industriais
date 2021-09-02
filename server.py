import socket
import socketserver, time
from time import sleep
import sys

host = '25.93.32.9'
port = 1234

timeout = 180
buffer_size = 1024

CONFIRMATION = bytes('ACK', 'utf-8')
NO_DATA = bytes('no_data', 'utf-8')

messages = []
FIRST_ITER = True

def control_client(mv):

    broadcastIP = '25.93.32.9'     #será usado pelo cliente para mandar os pacotes 
    serverPORT = 9888              #Porta em que envia dados ao Servidor Atuador
    
    # Criação de uma socket UDP para o cliente enviar para o servidor
    c = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    c.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    print('Socket inicializada com sucesso!')

    #c.bind((broadcastIP,serverPORT))
    print('Bind da socket realizada com sucesso!')

    control_message = control(mv, 0, 600, 0, 2000)
    control_message = int.to_bytes(control_message, 4, byteorder = 'little')
    print('MV: ', control_message)                    

    c.sendto(control_message,(broadcastIP,serverPORT))
    
    c.close()
    
def control(x, in_min, in_max, out_min, out_max):
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

def convert(pv):
    vout = (pv * 0.0048828125)
    r_ldr = (10000.0 * (5 - vout))/vout
    lux = (r_ldr/500)
    
    return lux

def setup():
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    
    server.settimeout(timeout)
    server.bind((host, port))

    print('Server connected...')
    
    return server

def receive_msg(server, fail_state_count = 0):
    
    global messages
    global FIRST_ITER
    
    while True:

        message, address = server.recvfrom(1024)
        
        print('message: ', message)
        print('from: ', address)
        
        identifier = message[:1].decode()
        PV_bytes = message[1:]
        
        if identifier == 'S':
            fail_state_count = 0
            
            PV_int = int.from_bytes(PV_bytes, 'little')
            PV = convert(PV_int)
            
            messages.append(PV)
            
            server.sendto(CONFIRMATION, address)
            
            print('PV = ', PV, ' Lux')
            
        elif identifier == 'A':
            if FIRST_ITER:
                FIRST_ITER = False
                messages = []
                
            else:
                if len(messages) != 0:

                    MV = int(messages[0])
                    messages.pop(0)
                    newmv = MV + 20

                    if MV < 0:
                        newmv = MV + 30

                    control_client(newmv)

                else:
                    server.sendto(NO_DATA, address)
                    fail_state_count = fail_state_count + 1 

                    print('No data sent to actuator')

                    if fail_state_count == 10:
                        server.sendto(int.to_bytes(0, 4, 'little'), address)
                        print('Fail state activated')
                        sys.exit(1)

        else:
            print('Cant interpretate request')
            
        print('--------------------')
        time.sleep(1)
        
server = setup()

receive_msg(server)