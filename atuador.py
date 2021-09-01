import socketserver
import socket
import time
import sys
import os
from threading import Thread
import serial

ARDUINO_PORT = 'COM3'
HOST    = '25.93.32.9'                      # IP do hamachi
PORT    = 1234
PERIOD  = 500                                   
NAME    = b'A'                                  # Nome do serviço 
BUFFER  = 1024
SERVER = (HOST, PORT)

def connect_client():
    
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    client.settimeout(5)

    print('Client connected...')
    
    return client

def connect_arduino():
    return serial.Serial(port=ARDUINO_PORT, baudrate = 9600, timeout=1)

def send_message(client):
        
    while True:

        client.sendto(NAME, (HOST, PORT))
        
        response, address = client.recvfrom(1024)
        
        value = int.from_bytes(response, 'little')
        
        print('Recebido: ', value)
        
        if value != 'no_data':
            pass
            #actuator.write(value)
        else:
            pass
        
        time.sleep(1.5)
        
client = connect_client()
#actuator = connect_arduino()

send_message(client)