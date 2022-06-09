# SISTEMAS DISTRIBUIDOS 2021-22
# PRACTICA 3
# JOSE IGNACIO DEL MORAL RODRIGUEZ

########################## SISTEMA DE GESTIÓN DE USUARIO #################################

# @post('/inicializar')
# @post('/almacenar') //Desactivado Temporalmente
# Menu0- @post('/usuario')
# Menu1- @post('/addRoom')
# Menu2- @post('/showInformationRoom/<roomId>')
# x- @post('/showInformationRoom/all')
# Menu3- @post('/addBooking')
# Menu4- @post('/showBookings/<userDNI>')
# Menu5- @post('/deteleBooking/<bookingId>')

from decimal import DefaultContext
import json
import os
import requests
import datetime


puerto = '''8080'''
direccion = '''http://localhost:'''
servidor = direccion + puerto

class cliente:
    def __init__(self, userName: str, password: str):
        self.userName = userName
        self.password = password


    def clearP(self):
        if os.name == "posix":
            os.system ("clear")
        elif os.name == "ce" or os.name == "nt" or os.name == "dos":
            os.system ("cls")

    def pausaP(self):
        pausa = input("\n\nPor favor, pulsa ENTER para continuar....")

    def Menu0(self, userName: str, password: str):

        data = {"userName": userName, "password": password}
        response = requests.post(url=servidor + '''/usuario''', json=data)
        datosJSON = json.loads(response.text)
        print(datosJSON)
        self.pausaP()
        if datosJSON["ERROR"] == 0:
            h.userName = userName
            h.password = password
        else:
            h.userName = ''
            h.password = ''

    # addRoom
    def Menu1(self, capacity: int, Resources: list):

        data = {"capacity": capacity, "password": Resources, "userName": h.userName, "password": h.password}

        response = requests.post(url=servidor + '''/addRoom''', json=data)
        datosJSON = response.content.decode('utf-8')
        print(datosJSON)
        self.pausaP()

    # showInformationRoom
    def Menu2(self, roomId: int):

        data = {"userName": h.userName, "password": h.password}

        response = requests.post(url=servidor + '''/showInformationRoom/''' + str(roomId), json=data)
        datosJSON = response.content.decode('utf-8')
        print(datosJSON)
        self.pausaP()

    # addBooking
    def Menu3(self, roomId: int, date: str, startTime: str, endTime: str):

        data = {"userName": h.userName, "password": h.password, "roomId": roomId, "date": date, "startTime": startTime, "endTime": endTime}

        response = requests.post(url=servidor + '''/addBooking''', json=data)
        datosJSON = response.content.decode('utf-8')
        print(datosJSON)
        self.pausaP()

    # showBookings    
    def Menu4(self, dni: str):

        data = {"userName": h.userName, "password": h.password}

        response = requests.post(url=servidor + '''/showBookings/''' + dni, json=data)
        datosJSON = response.content.decode('utf-8')
        print(datosJSON)
        self.pausaP()

    # deteleBooking
    def Menu5(self, bookingId: str):

        data = {"userName": h.userName, "password": h.password}

        response = requests.post(url=servidor + '''/deleteBooking/''' + bookingId, json=data)
        datosJSON = response.content.decode('utf-8')
        print(datosJSON)
        self.pausaP()

    # EXTRA. Listado de todas las Salas
    def MenuExtra(self):

        data = {"userName": h.userName, "password": h.password}
        response = requests.post(url=servidor + '''/showInformationRoom/all''', json=data)
        json_data = json.loads(response.content.decode('utf-8'))
        for dato in json_data:
            print(dato)
        self.pausaP()


h = cliente('','')



def main():
    global h

    h.clearP()
    response = requests.post(url=servidor + '''/inicializar''')
    datosJSON = json.loads(response.text)
    print(datosJSON)
    h.pausaP()


    opcion = '0'
    while opcion != '6':
        h.clearP()
        seguir = True        
        print( "####### SISTEMA DE GESTION DE SALAS #######\n\n")
        if (h.userName==''):
            print("Usuario no identificado.\n")
        else:
            print("Bienvenido usuario:{}\n".format(h.userName))
            
        print('''Opciones:
            0. Identificacion del USUARIO
            1. Añadir Sala
            2. Mostrar Información de Sala
            3. Añadir Reserva
            4. Listar Reserva
            5. Eliminar Reserva
            6. Salir
            7. EXTRA. Mostrar la información de Todas las Salas.\n''')
        opcion = input('Elija una opcion: ')

        if opcion == '0':     # IDENTIFICACIÓN DEL USUARIO
            try:
                h.userName = input('Introduce el nombre de USUARIO : ')
                h.password = input('Introduce la password : ')
            except Exception as e:
                print("Error al introducir datos: {}".format(str(e)))
                seguir = False                
            
            if len(h.userName) > 0 and len(h.password) > 0 and seguir == True:
                h.Menu0(h.userName, h.password)

        elif opcion == '1':   # DAR DE ALTA UNA SALA
            try:
                capacity = int(input('Introduce la capacidad de la Sala : '))
                Resources = input('Introduce los recursos separados por coma : ').split(",")
            except Exception as e:
                print("Error al introducir datos: {}".format(str(e)))
                seguir = False
            
            if seguir == True:            
                h.Menu1(capacity, Resources)

        elif opcion == '2':   # MOSTAR UNA UNA SALA
            try:
                roomId = int(input('Introduce el identificador de la Sala : '))
            except Exception as e:
                print("Error al introducir datos: {}".format(str(e)))
                seguir = False
            
            if seguir == True:
                h.Menu2(roomId)
        
        elif opcion == '3':   # DAR DE ALTA UNA RESERVA
            try:
                roomId = int(input('Introduce el identificador de la Sala : '))
                date = input('Introduce una fecha DD/MM/YYYY : ')
                startTime = input('Introduce una hora de Comienzo HH:MM : ')
                endTime = input('Introduce una hora de finalizacion HH:MM : ')
            
                fecha1 = date.split("/")
                hora1 = startTime.split(":")
                hora2 = endTime.split(":")    
                      
                _t_start = datetime.time(int(hora1[0]), int(hora1[1]))
                t_end = datetime.time(int(hora2[0]), int(hora2[1]))
                t_fecha1 = datetime.date(int(fecha1[2]), int(fecha1[1]), int(fecha1[0]))

            except Exception as e:
                print("Error al introducir datos: {}".format(str(e)))
                seguir = False
                h.pausaP()
            
            if seguir == True:
                h.Menu3(roomId, date, startTime, endTime)
        
        elif opcion == '4':   # BUSCAR RESERVAS POR DNI
            try:
                dni = input('Introduce el DNI de la persona que realizó la reserva 00000000X : ')
            except Exception as e:
                print("Error al introducir datos: {}".format(str(e)))
                seguir = False
                
            if seguir == True:
                h.Menu4(dni)

        elif opcion == '5':   # ELMINAR UNA RESERVA
            try:
                bookingId = input('Introduce el identificador de la Reserva: ')
            except Exception as e:
                print("Error al introducir datos: {}".format(str(e)))
                seguir = False
                
            if seguir == True:
                h.Menu5(bookingId)
        
        elif opcion == '6':
            print('Finalizando programa...')

        elif opcion == '7':   # EXTRA. MOSTAR TODAS LAS SALAS
            try:
                h.MenuExtra()
            except Exception as e:
                print("Error al acceder al listado: {}".format(str(e)))
            
        else:
            print('Error: la opcion introducida es invalida')


# Llama a main()
if __name__ == '__main__':
    main()
