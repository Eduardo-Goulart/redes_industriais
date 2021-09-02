from sockets_udp.udp_client import Client
from serial_ard.serial_ard import Serial_sr
from struct import pack
import socketserver
import socket
import time
import sys
import os
from threading import Thread
import serial
import numpy as np
from random import randint

COMPORT = 'COM3'
HOST    = '25.93.32.9'                        # IP do hamachi
PORT    = 1234
PERIOD  = 500                                   # Periodo do ciclo em ms
NAME    = b'S'                                   # Nome do serviço 
buffer = 1024
C_PORT = 5555

def connect():
    
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    
    client.settimeout(5)
    client.bind((HOST, C_PORT))  ## C_PORT É UMA PORTA FIXA DEFINIDA NO CÓDIGO
    print('Client connected...')
    
    return client

def connect_arduino():
    return serial.Serial(port = COMPORT, baudrate = 9600, timeout = 1)

def send_message(client):
    
    while True:
        
        valor_sensor = randint(1, 10)
        
#         valor_sensor = int(arduino.readline())
        
        bytes_to_send = int.to_bytes(valor_sensor, 3, byteorder='little')
        PV = NAME + bytes_to_send
        
        print('Sending: ', PV)
        
        client.sendto(PV, (HOST, PORT))
        
        response, address = client.recvfrom(1024)
        
        print('Response: ', response.decode())
        
        time.sleep(1.0)
        
client = connect()
#arduino = connect_arduino()

send_message(client)