# client.py
# Fuente: https://recursospython.com/codigos-de-fuente/enviar-archivo-via-socket-en-python-3/

import os
import socket
import struct

HOST = 'localhost'
PORT = 2001

def send_file(sck: socket.socket, filename):
    # Obtener el tamaño del archivo a enviar.
    filesize = os.path.getsize(filename)
    # Informar primero al servidor la cantidad
    # de bytes que serán enviados.
    sck.sendall(struct.pack("<Q", filesize))
    # Enviar el archivo en bloques de 1024 bytes.
    with open(filename, "rb") as f:
        while read_bytes := f.read(1024):
            sck.sendall(read_bytes)


fich = input("Introduce el nombre del archivo a enviar con la extensión: ")

# Nos aseguramos de que existe ese archivo
try:
    os.path.exists(filename)
except OSError:
    raise

conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
REMOTE_ADDR = (HOST, PORT)

# Estableceremos conexión TCP
conn.connect(REMOTE_ADDR)

# en TCP no hay que especificar la tupla
print("Enviando Nombre del archivo...")
conn.send(filename.encode("utf-8"))
print("Enviando archivo...")

# Llamamos a la función funcion
send_file(conn, fich)
print("Enviado.")

conn.close()
print("Conexión cerrada.")