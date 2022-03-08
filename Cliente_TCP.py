# Cliente TCP
import socket

# Dirección donde está el servidor
REMOTE_PORT = 2001
REMOTE_HOST = 'localhost'

# PROTOCOLO: AF_INET -> IPV4
# # UDP -> SOCK_DGRAM
# # TCP -> SOCK_STREAM
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
REMOTE_ADDR = (REMOTE_HOST, REMOTE_PORT)

# Estableceremos conexión TCP
s.connect(REMOTE_ADDR)

# en TCP no hay que especificar la tupla
s.send("Un pequeño mensaje.".encode("utf-8"))

buffer = s.recv(1024)
print("Mensaje recibido: '" + buffer.decode("utf-8")
      + str(REMOTE_ADDR))

s.close()