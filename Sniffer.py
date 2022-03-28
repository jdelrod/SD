# Sniffer para LINUX (Ejecutar con privilegios de Administrador)
# Version TCP
# https://www.binarytides.com/python-packet-sniffer-code-linux/

import socket
import sys
from struct import *

# Puerto de RX/TX de los protocolos TCP/UDP
PORT = 65535

# INET -> IPv4
# Probaremos que se puede abrir ese socket. En caso contrario, genera un error.
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
except socket.error:
    print('El socket no puede ser creado. Error.')
    raise

#Capturando....
while True:
    # Almacenamos en una tupla los datos recibidos.
    buffer = s.recvfrom(PORT)
    # De la tupla, almacenamos [0] que es el paquete
    packet = buffer[0]

    # Almacenamos los 20 Bytes del IP-Header
    ip_header = packet[0:20]

    # CABECERA IP
    iph = unpack('!BBHHHBBH4s4s', ip_header)

    version_ihl = iph[0]
    version = version_ihl >> 4
    ihl = version_ihl & 0xF

    iph_length = ihl * 4
    ttl = iph[5]
    protocol = iph[6]
    s_addr = socket.inet_ntoa(iph[8])
    d_addr = socket.inet_ntoa(iph[9])

    print('Version : ' + str(version)
          + ' IP Header Length : ' + str(ihl)
          + ' TTL : ' + str(ttl)
          + ' Protocol : ' + str(protocol)
          + ' Source Address : ' + str(s_addr)
          + ' Destination Address : ' + str(d_addr))

    tcp_header = packet[iph_length:iph_length + 20]

    # CABECERA TCP
    tcph = unpack('!HHLLBBHHH', tcp_header)

    source_port = tcph[0]
    dest_port = tcph[1]
    sequence = tcph[2]
    acknowledgement = tcph[3]
    doff_reserved = tcph[4]
    tcph_length = doff_reserved >> 4

    print('Source Port : ' + str(source_port)
          + ' Dest Port : ' + str(dest_port)
          + ' Sequence Number : ' + str(sequence)
          + ' Acknowledgement : ' + str(acknowledgement)
          + ' TCP header length : ' + str(tcph_length))

    h_size = iph_length + tcph_length * 4
    data_size = len(packet) - h_size

    # Capturamos los datos del paquete
    data = packet[h_size:]

    print('Data : ' + str(data))
    print()

# Cerramos el socket
s.close()
