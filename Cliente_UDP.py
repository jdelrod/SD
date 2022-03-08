# Cliente UDP
import socket

#Pondremos los datos del Servidor donde queremos conectarnos
PORT = 2000
HOST = 'localhost'

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# TCP -> send
# UDP -> send
s.sendto("Soy el Cliente UDP.".encode("utf-8"), (HOST, PORT))

buffer, addr_c = s.recvfrom(1024)
print("Recibido: '" + buffer.decode("utf-8") + " de la Dir: " + str(addr_c))
