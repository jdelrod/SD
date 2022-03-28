# Servidor. Recibe un archivo.
#Fuente: https://programmerclick.com/article/1442863978/

import os
import socket
import struct

LOCAL_IP = 'localhost'   # La dirección de esta máquina en la red de área local, o escriba 127.0.0.1
PORT = 2567              # Especifique un puerto

def server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # socket.AF_INET se refiere al socket ipv4.SOCK_STREAM usando el protocolo tcp
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Establecer el puerto
    sock.bind((LOCAL_IP, PORT))       # Puerto de enlace
    sock.listen(3)                    # Puerto de escucha
    while True:
        sc,sc_name = sock.accept()    # Cuando hay una solicitud para el puerto especificado, accpte () devolverá un nuevo socket y el host (ip, port)
        print('Recibió {} solicitud'.format(sc_name))
        infor = sc.recv(1024)       # Primero reciba un dato, este dato contiene la longitud del archivo y el nombre del archivo, separados por |, las reglas específicas se pueden especificar en el cliente
        length,file_name = infor.decode().split('|')
        if length and file_name:
            newfile = open('image/'+str(random.randint(1,10000))+'.jpg','wb')  # El nombre de archivo analizado desde el cliente se puede usar aquí
            print('length {},filename {}'.format(length,file_name))
            sc.send(b'ok')   # Indica la longitud del archivo recibido y el nombre del archivo
            file = b''
            total = int(length)
            get = 0
            while get < total:         #Recibir archivos
                data = sc.recv(1024)
                file += data
                get = get + len(data)
            print('Debería recibir {}, en realidad recibir {}'.format(length,len(file)))
            if file:
                print('acturally length:{}'.format(len(file)))
                newfile.write(file[:])
                newfile.close()
                sc.send(b'copy')    #Diga el archivo completo recibido
        sc.close()

