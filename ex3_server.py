import argparse
import socket


def main(host, port):
    # Creamos conexión AF_INET->IPV4, DGRAM->UDP
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((host, port))

    jugador = []
    conexion = []
    tablero = []
    juego = []
    barcos = []

    # Recibimos  el nombre y tablero de cada jugador
    for a in range(0, 2):
        buffer, addr_c = s.recvfrom(512)
        jugador.append(str(buffer.decode("utf-8")))
        print("Jugador : {name}".format(name=jugador[a]))

        buffer, addr_c = s.recvfrom(512)
        data = str(buffer.decode("utf-8"))
        barcos.append(data.count("1"))
        data = data.split(';')

        for i in range(0, 10):
            tablero.append(list(data[i].split()))
            print(tablero[i])

        # Se añade el tablero en la lista
        juego.append(tablero)

        print("Barcos del jugador ({x}): {bar}\n".format(x=a, bar=barcos[a]))

        # Se almacenará la tupla de direccion y puerto de cada jugador
        conexion.append(addr_c)

    # Inicio del juego.
    barcosjugador1 = barcos[0]
    barcosjugador2 = barcos[1]
    letras = "ABCDEFGHIJ"
    xjugador = 0
    xatacado = 1
    contador = 0
    ganador = 0
    perdedor = 0
    finished = False
    agua = False

    while not finished:
        while not agua:
            contador = contador + 1
            # Enviamos turno
            data = "Turn " + str(contador)
            s.sendto(data.encode("utf-8"), conexion[xjugador])

            # Esperando ataque..
            buffer, addr_c = s.recvfrom(512)
            dato = str(buffer.decode("utf-8"))

            # Extraemos el valor del buffer
            columna = int(letras.find(dato[0:1]))
            fila = int(dato[1:])

            ataque = juego[xatacado][fila][columna]

            if ataque == "0":
                data = "Fail"
                agua = True
            else:
                data = "Hit"
                juego[xatacado][fila][columna-1] = "0"
                if xatacado == 1:
                    barcosjugador2 = barcosjugador2 - 1
                else:
                    barcosjugador1 = barcosjugador1 - 1

            # Si no hay barcos... entonces acabó el juego
            if barcosjugador1 == 0 or barcosjugador2 == 0:
                finished = True
                ganador = xjugador
                perdedor = xatacado
                break

            s.sendto(data.encode("utf-8"), conexion[xjugador])

        # Volvemos a poner el valor de agua a False
        agua = False

        # Cambiamos de atacante
        if xjugador == 0:
            xjugador = 1
            xatacado = 0
        else:
            xjugador = 0
            xatacado = 1

    print("Ganador: {J1} , Perdedor: {J2}".format(J1=jugador[ganador], J2=jugador[perdedor]))
    s.sendto("You win".encode("utf-8"), conexion[ganador])
    s.sendto("You lost".encode("utf-8"), conexion[perdedor])
    s.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', default=1024, help="listening port")
    parser.add_argument('--host', default='localhost', help="hostname")
    args = parser.parse_args()
    print("Escuchando... {port}, {host}".format(port=args.port, host=args.host))
    main(args.host, args.port)
