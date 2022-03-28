# Server.py
# Fuente: https://recursospython.com/codigos-de-fuente/enviar-archivo-via-socket-en-python-3/

import socket
import struct

HOST = 'localhost'
PORT = 2001

def receive_file_size(sck: socket.socket):
    # Esta función se asegura de que se reciban los bytes
    # que indican el tamaño del archivo que será enviado,
    # que es codificado por el cliente vía struct.pack(),
    # función la cual genera una secuencia de bytes que
    # representan el tamaño del archivo.
    fmt = "<Q"
    expected_bytes = struct.calcsize(fmt)
    received_bytes = 0
    stream = bytes()
    while received_bytes < expected_bytes:
        chunk = sck.recv(expected_bytes - received_bytes)
        stream += chunk
        received_bytes += len(chunk)
    filesize = struct.unpack(fmt, stream)[0]
    return filesize


def receive_file(sck: socket.socket, fich):
    # Leer primero del socket la cantidad de
    # bytes que se recibirán del archivo.
    filesize = receive_file_size(sck)
    # Abrir un nuevo archivo en donde guardar
    # los datos recibidos.
    with open(fich, "wb") as f:
        received_bytes = 0
        # Recibir los datos del archivo en bloques de
        # 1024 bytes hasta llegar a la cantidad de
        # bytes total informada por el cliente.
        while received_bytes < filesize:
            chunk = sck.recv(1024)
            if chunk:
                f.write(chunk)
                received_bytes += len(chunk)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()
print("Esperando al cliente...")
conn, address = server.accept()
print(f"{address[0]}:{address[1]} conectado.")
print("Recibiendo nombre del archivo...")
# Como es TCP -> recv
buffer = conn.recv(1024)
fich = str(buffer.decode("utf-8"))
print("Recibiendo archivo..." + fich)

# Llamamos a la funcion
receive_file(server, fich)
print("Archivo recibido.")

server.close()
print("Conexión cerrada.")