# Servidor UDP
import socket

# Puertos <1024 reservados
PORT = 2000
HOST = 'localhost' #192.168.56.1'

# PROTOCOLO: AF_INET -> IPV4
# # UDP -> SOCK_DGRAM
# # TCP -> SOCK_STREAM

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

s.bind((HOST, PORT)) # Hacemos que use un puerto concreto, aunque luego se reencaminen a otro
# El servidor se queda a la espera de recibir conexion
print("Esperando conexión...")

# UDP -> recvfrom
# TCP -> recv
buffer, addr_c = s.recvfrom(1024) # Método bloqueante. Recibimos una tupla.
#print("Recibido mensaje: " + buffer.decode("utf-8") + " de la dirección: " + str(addr_c))
#Como addr_c es una tupla, lo separamos por elementos:
print("Recibido mensaje: " + buffer.decode("utf-8")
      + " de la dirección IP: " + str(addr_c[0])
      + " Puerto: " + str(addr_c[1]))

#Enviamos OK
s.sendto("Fin de la transmisión cliente.".encode("utf-8"), addr_c) #Enviamos una tupla

# Prueba de cifrado de datos
buffer, addr_c = s.recvfrom(1024)
X = "aeiou"
Y = "12345"
translation_table = str.maketrans(Y, X)
texto = buffer.decode("utf-8").translate(translation_table)
print(texto)

#cerramos el socket
s.close()