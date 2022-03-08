# Servidor TCP
import socket

PORT = 2001
HOST = 'localhost'

# Creamos un socket, como es un TCP será con SOCK_STREAM
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Puerto de escucha definido, pero de recepción aleatorio. Recibimos Tupla.
s.bind((HOST, PORT))

print("Escuchando a través del puerto: " + str(PORT))
# Escuchamos los procesos y cuando se reciban pasamos del PORT al puerto aleatorio.
s.listen()

# Si OK pasamos de un puerto a otro.. se acepta!
# HOST del cliente y PORT del cliente
# La dirección del cliente sólo se recibe cuando se establece la conexión, no en cada mensaje.
socket_c, addr_c = s.accept()

# Como es TCP -> recv
buffer = socket_c.recv(1024)
print("Recibido mensaje '" + buffer.decode("utf-8") +
      "' de la IP: " + str(addr_c[0]) +
      " Puerto: " + str(addr_c[1]))

#como sabemos el IP del cliente, solo es necesario enviar una respuesta al socket abierto
socket_c.send("Fin de recepción.".encode("utf-8"))

s.close()
