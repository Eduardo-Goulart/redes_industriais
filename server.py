import socket
import socketserver, time
from threading import Thread
from time import sleep
import sys

host = '25.93.32.9'  #http://25.94.218.230:555
port = 1234

timeout = 180
buffer_size = 1024

CONFIRMATION = bytes('Data processed', 'utf-8')
NO_DATA = bytes('no_data', 'utf-8')
EMPTY_DATA = b'no_data'

# broadcast = ('<broadcast>', 1234)

messages = []
FIRST_ITER = True

def control(x, in_min, in_max, out_min, out_max):
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

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
        print('listening')
        message, address = server.recvfrom(1024)
        
        print('message: ', message)
        print('from: ', address)
        
        identifier = message[:1].decode()
        PV_bytes = message[1:]
        
        if identifier == 'S':
            fail_state_count = 0
            
            PV_int = int.from_bytes(PV_bytes, 'little')
            messages.append(PV_int)

            server.sendto(CONFIRMATION, address)
            
            print('PV = ', PV_int)
            
        elif identifier == 'A':
            
            if FIRST_ITER:
                messages = []
                FIRST_ITER = False
            else:
                if len(messages) != 0:

                    to_send = messages[0]
                    messages.pop(0)

                    print('Sending: ', to_send)

#                     MV = control(to_send, 50, 100, 0, 100)

                    # SIMULACAO
                    MV = control(to_send, 0, 10, 0, 100)

                    bytes_to_send = int.to_bytes(MV, 4, byteorder = 'little')
                    server.sendto(bytes_to_send, address)

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
            
        time.sleep(0.5)
        
server = setup()

receive_msg(server)