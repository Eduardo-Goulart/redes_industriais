import socketserver
import socket
import time
import sys
import os
from threading import Thread
import serial
import pyfirmata
from random import randint

HOST    = '25.93.32.9'                        # IP do hamachi
PERIOD  = 500                                   
NAME    = b'A'                                # Nome do serviço 
BUFFER  = 1024
SERVER = (HOST, PORT)
PORT    = 9888

def connect_client():
    
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    client.settimeout(15)
    client.bind((HOST, PORT))   # PORT É UMA PORTA FIXA DEFINIDA EM CÓDIGO
    print('Client connected...')
    
    return client

def send_message(client):
        
    while True:
        
        client.sendto(NAME, (HOST, 1234))
        print('\n\n*****************')
        response, address = client.recvfrom(1024)
        print('',response)
        value = int.from_bytes(response, 'little')
        
        print('Recebido: ', value)
        
        if value != 'no_data':
#             led.write(random_float)
            pass
        else:
            pass
        
        time.sleep(0.5)
        
        
client = connect_client()
send_message(client)
        
