# Servidor TCP
import socket
import argparse
import os


def main(host, port):

    # Creamos conexión AF_INET->IPV4, STREAM->TCP
    socket_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Puerto de escucha definido, pero de recepción aleatorio. Recibimos Tupla.
    local_addr = (host, port)
    socket_s.bind(local_addr)
    socket_s.listen()
    socket_s, addr_c = socket_s.accept()

    # letra a buscar
    letra = 'a'
    contador = 0
    listadepalabras = []
    fin = ""

    while fin != "@FIN":
        buffer = str((socket_s.recv(512)).decode("utf-8")).split()
        for palabra in buffer:
            if letra in palabra:
                contador = contador + 1
                listadepalabras.append(palabra)
        if palabra == "@FIN":
            buffer.pop()
            fin = "@FIN"
        print(buffer)

    # Enviamos al cliente el total y palabras con el criterio especificado
    socket_s.send((str(contador)).encode("utf-8"))

    # Enviamos al cliente las palabras
    for palabra in listadepalabras:
        socket_s.send((str(palabra + "\n")).encode("utf-8"))

    # Enviamos al cliente la señal de FIN de la transmisión
    socket_s.send("@FIN".encode("utf-8"))

    socket_s.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', default=1025, help="listening port")
    parser.add_argument('--host', default='localhost', help="hostname")
    args = parser.parse_args()
    print("Escuchando... {port}, {host}".format(port=args.port, host=args.host))
    main(args.host, args.port)
