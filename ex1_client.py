# Cliente UDP
import argparse
import socket
import math
import random

def montecarlo(s, host, port, n):
    below_counter = 0
    for i in range(0, n):
        x = random.uniform(0, 1)
        y = random.uniform(0, 1)
        s.sendto(("(" + str(x) + "," + str(y) + ")").encode("utf-8"), (host, port))
        buffer, addr_c = s.recvfrom(512) #Recibimos Tupla
        datos = str(buffer.decode("utf-8"))
        if datos == "below":
            below_counter = below_counter + 1

    pi = 4.0 * float(below_counter) / float(n)
    return pi

def main(host, port, n):
    # Creamos conexión AF_INET->IPV4, DGRAM->UTP
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # enviamos la conexión y datos a la función montecarlo
    pi = montecarlo(s, host, port, n)
    print("El valor aproximado de PI con: " + str(n) + " puntos aleatorios es: " + str(pi))
    s.sendto("exit".encode("utf-8"), (host, port))
    # cerramos socket
    s.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', default=1024, help="remote port")
    parser.add_argument('--host', default='localhost', help="remote hostname")
    parser.add_argument('--number', default=100000, help="number of random points to be generated")
    args = parser.parse_args()
    print("Estableciendo conexión con: {port}, {host}".format(port=args.port, host=args.host))
    print("Número de puntos aleatorios: {number}".format(number=args.number))
    main(args.host, args.port, args.number)
