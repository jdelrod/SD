# Cliente UDP
import socket

#Pondremos los datos del Servidor donde queremos conectarnos
PORT = 2000
HOST = 'localhost' #192.168.56.1

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# TCP -> recv     send
# UDP -> recvfrom sendto
s.sendto("Soy el Cliente UDP.".encode("utf-8"), (HOST, PORT))

buffer, addr_c = s.recvfrom(1024)
print("Recibido: '" + buffer.decode("utf-8") + " de la Dir: " + str(addr_c))

# Prueba de cifrado de datos
X = "aeiou"
Y = "12345"
translation_table = str.maketrans(X, Y)
texto = "Hola esto es una prueba"
s.sendto(texto.translate(translation_table).encode("utf-8"), (HOST, PORT))

# Cerramos socket
s.close()
