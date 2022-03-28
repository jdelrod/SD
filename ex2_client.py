# Cliente TCP
import socket
import argparse
import os


def main(host, port, filein, fileout):
    # Comprobamos si existe el fichero a enviar
    try:
        os.path.exists(filein)
    except OSError:
        raise

    # Creamos conexión AF_INET->IPV4, STREAM->TCP
    socket_c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    dir_remota = (host, port)

    # Estableceremos conexión TCP
    socket_c.connect(dir_remota)
    print("Conectado.")

    with open(filein, 'r') as in_file:
        for line in in_file:
            socket_c.sendall((str(line)).encode("utf-8"))
        socket_c.sendall("\n@FIN".encode("utf-8"))

    fin = ""
    letra = "a"
    buffer = socket_c.recv(512)
    contador = str(buffer.decode("utf-8"))
    print("El número de palabras que contienen la letra '{letrabus}' es {cont}.".format(letrabus=letra, cont=contador))

    # Comprobamos si se puede abrir un archivo para escritura
    try:
        with open(fileout, 'w') as out_file:
            while fin != "@FIN":
                buffer = str(socket_c.recv(512).decode("utf-8")).split()
                for palabra in buffer:
                    if palabra == '@FIN':
                        fin = "@FIN"
                    else:
                        out_file.write(palabra + '\n')

    except FileNotFoundError:
        print("No existe el fichero: " + fileout)

    socket_c.close()
    out_file.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', default=1025, help="remote port")
    parser.add_argument('--host', default='localhost', help="remote hostname")
    parser.add_argument('--filein', default='filein.txt', help="file to be read")
    parser.add_argument('--fileout', default='fileout.txt', help="file to be written")
    args = parser.parse_args()
    print("Estableciendo conexión con: {port}, {host}".format(port=args.port, host=args.host))
    print("Fichero a enviar: {filein}".format(filein=args.filein))
    print("Fichero de Salida: {fileout}".format(fileout=args.fileout))
    main(args.host, args.port, args.filein, args.fileout)
