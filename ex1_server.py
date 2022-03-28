# Servidor UDP
import argparse
import socket
import math
import random

def f(x):
    return math.sqrt(1 - math.pow(x, 2))

def main(host, port):
    # Creamos conexión AF_INET->IPV4, DGRAM->UDP
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((host, port))
    print("Waiting for messages...")

    while True:
        #establecemos el tamaño del buffer como 512
        buffer, addr_c = s.recvfrom(512)
        datos = eval(str(buffer.decode("utf-8"))) #Evaluamos el contenido del buffer

        #Si dato recibido es exit salimos del bucle while
        if datos == "exit":
            break

        x, y = float(datos[0]), float(datos[1])
        if y < f(x) and y > 0 and y < 1:
            s.sendto("below".encode("utf-8"), addr_c)  #Enviamos una tupla
        else:
            if y > f(x) and y > 0 and y < 1:
                s.sendto("above".encode("utf-8"), addr_c)  # Enviamos una tupla
            else:
                s.sendto("error".encode("utf-8"), addr_c)  # Enviamos una tupla

        print(x, y)

    print("Recibido el comando {salir}.".format(salir=datos))
    s.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', default=1024, help="listening port")
    parser.add_argument('--host', default='localhost', help="hostname")
    args = parser.parse_args()
    print("Escuchando... {port}, {host}".format(port=args.port, host=args.host))
    main(args.host, args.port)
