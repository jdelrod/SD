#Cliente. Envia un fichero.
#Fuente: https://programmerclick.com/article/1442863978/

import os
import socket
import struct

LOCAL_IP = 'localhost'   # La dirección de esta máquina en la red de área local, o escriba 127.0.0.1
PORT = 2567              # Especifique un puerto

address = (LOCAL_IP, PORT)

def send(photos):
    for photo in photos[0]:
        print('sending {}'.format(photo))
        data = file_deal(photo)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(address)
        sock.send('{}|{}'.format(len(data),
                                 file).encode())  # Codificación predeterminada utf-8, enviar longitud de archivo y nombre de archivo
        reply = sock.recv(1024)
        if 'ok' == reply.decode():  # Confirme que el servidor obtiene la longitud del archivo y los datos del nombre del archivo
            go = 0
            total = len(data)
            while go < total:  # Enviar archivo
                data_to_send = data[go:go + 1024]
                sock.send(data_to_send)
                go += len(data_to_send)
            reply = sock.recv(1024)
            if 'copy' == reply.decode():
                print('{} send successfully'.format(photo))
        sock.close()  # Debido a que tcp transmite datos en forma de flujo, no podemos juzgar el principio y el final. La forma simple es usar un socket sin transmitir un archivo, pero esto es un consumo de recursos informáticos. Los bloggers están explorando mejores métodos. Oportunidad para comunicarse


def file_deal(file_path):  # Leer método de archivo
    mes = b''
    try:
        file = open(file_path, 'rb')
        mes = file.read()
    except:
        print('error{}'.format(file_path))
    else:
        file.close()
        return mes
