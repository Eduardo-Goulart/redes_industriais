import socket

class Client:

    HOST    = '127.0.0.1'     # IP address 
    PORT    = 5000            # Port where the server is connected
    TIMEOUT = 5               # Timeout in seconds 
    BUFF    = 1024            # Buffer to receive n bytes 

    def __init__(self, HOST, PORT, timeout = 5):

        self.HOST     = HOST
        self.PORT       = PORT  
        self.TIMEOUT  = timeout
        self.BUFF     = 1024

        self.isAlive = False 

        # Cria o socket TCP 
        self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.udp.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        if self.TIMEOUT:                        # Seta o Timeout para bloqueante ou não bloqueante 
            self.udp.settimeout( self.TIMEOUT ) # Timeout garante que a conexão irá durar esse tempo

        self.server_addr = (HOST, PORT)           # Cria a tupla addr do server
        self.connect_server()                   # Chama o método de conexão do servidor


    """ Para se conectar em um servidor                                                  
    """
    def connect_server ( self ):
        try: 
            # Conecta no servidor no host e ip passados
            self.udp.connect( self.server_addr )
            print("Conectado com ", self.server_addr )
            self.isAlive = True 
        except:
            print("Falha para conectar no servidor : ", self.server_addr, " Chame novamente o método connect_server mais tarde" ) 
            self.isAlive = False 


    """ Para mandar uma mensagem TCP usar o método abaixo.
        Padrão usar mensagens str.encode() ou str. 
    """
    def send_message( self, msg ):
        # Garante que a mensagem esteja codificada
        if type(msg) is str:
            msg = msg.encode()
        elif type(msg) is not bytes:
            print("Dados fora do padrão de envio TCP != str or bytes")

        self.udp.sendto(msg, self.server_addr)


    """ Método para receber uma mensagem.
        Lembrar do timeout (segundos).
    """
    def receive_message(self, show_msg):

        try:
            msg = self.udp.recvfrom(self.BUFF)
            
            if show_msg:
                print("Receive : ", msg)
            return msg 
                
        except socket.timeout as err :
            
            if show_msg:
                print("Receive ", err)
            return None 

            
    """ setar o tamanho máximo do buffer.
    """
    def set_buffer(self, buff):
        self.BUFF = buff

    """
        Setar o timeout da conexão.
    """
    def set_timeout(self, timeout):
        self.TIMEOUT = timeout
        self.udp.settimeout( self.TIMEOUT )

    """ Encerrar a conexão TCP.
    """
    def close_connection(self):
        self.udp.close()