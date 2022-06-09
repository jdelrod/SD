# SISTEMAS DISTRIBUIDOS 2021-22
# PRACTICA 3
# JOSE IGNACIO DEL MORAL RODRIGUEZ

# Base de datos local: BaseDatos.json

# CARGA DE DATOS INICIALES
# Desde el cliente se realiza un POST al servidor para inicializar la BD:
# http://127.0.0.1:8080/inicializar

# COPIA DE SEGURIDAD
# Cada vez que se introduce o modifica un dato, se almacena localmente una copia de seguridad
# de la Base de Datos sobreescribiendo el fichero antiguo

# FUNCIONES
# 
# @post('/inicializar')
# @post('/almacenar') //Desactivado Temporalmente
# @post('/usuario')
# @post('/addRoom')
# @post('/showInformationRoom/<roomId>')
# @post('/showInformationRoom/all') //No disponible desde este cliente
# @post('/addBooking')
# @post('/showBookings/<userDNI>')
# @post('/deleteBooking/<bookingId>')


from bottle import run, request, response,post
import json
import datetime
import os

#Direccion y nombre del archivo de Base de Datos
directorio = str(os.getcwd())
basededatos = '/BaseDatos.json'
rutaBaseDatos = directorio + basededatos

# SISTEMA DE GESTIÓN DE RESERVAS
class Reservas:  
    def __init__(self):
        self.bd = {}
        self.Usuarios = {}
        self.bd['BD'] = []
        self.Usuarios['Usuarios'] =[]

    def contenido (self, roomId: int, capacity: int, Resources: list, user: list, datosReserva: list, ocupada: int, errorMessage: str, message: str):
        self.roomId = roomId # Sala
        self.capacity = capacity # Total capacidad sala
        self.Resources = Resources # Equipamiento disponible en sala
        self.user = user # dni, usuario, password
        self.datosReserva = datosReserva # datos de la reserva
        self.ocupada = ocupada # Marca de ocupación de sala
        self.errorMessage = errorMessage # Mensaje de error
        self.message= message # Mensage sobre la reserva

    def datosUsuarioActual(self, dni_: str, userName_: str, password_: str):
        self.dni_ = dni_
        self.userName_ = userName_
        self.password_ = password_

    def room(self, Id: list):
        self.Id = Id

    def inicioVariables(self):
        self.contenido(0, 0, ["","",""], ["","",""], ["", "", "", "", 0, ""], 0, "", "")
        self.room(["0","0"])
    
    def insertarsala(self, capacity: int, Resources: list):
        y = []       
        temp = dict()
        temp = self.bd
        for dato in temp:
            if dato['roomId'] not in y:
                y.append(dato['roomId']) #Almacenaremos las salas existentes en la BD sin repetición
            
        
        y.sort()
        total = y[-1]
                
        y.clear()
        
        self.contenido(total + 1, capacity, Resources, [self.dni_, self.userName_, self.password_], [str(total + 1) + "-0" ,"","","",0,""], 0, "", "")
        
        self.bd.append({'roomId': self.roomId,
                                'capacity': capacity,
                                'Resources': Resources,
                                'user': self.user,
                                'datosReserva': self.datosReserva,
                                'ocupada': self.ocupada,
                                'errorMessage': self.errorMessage,
                                'message': self.message})


    def cargarJSON(self):
        with open(rutaBaseDatos, 'r') as fichero:
            data = json.load(fichero)
            temp = {}         
            temp['BD'] = []
            for dato in data['BD']:
                temp['BD'].append({'roomId': dato['roomId'],
                                'capacity': dato['capacity'],
                                'Resources': dato['Resources'],
                                'user': dato['user'],
                                'datosReserva': dato['datosReserva'],
                                'ocupada': dato['ocupada'],
                                'errorMessage': dato['errorMessage'],
                                'message': dato['message']})
            self.bd = temp['BD']
            temp.clear()
            temp['Usuarios']= []
            for dato in data['Usuarios']:
                temp['Usuarios'].append({'user': dato['user']})
            
            self.Usuarios = temp['Usuarios']
            temp.clear()
            
        fichero.close()


    def guardarJSON(self):
        with open(rutaBaseDatos, 'w') as fichero:
            temp = dict()
            temp['Usuarios']= self.Usuarios
            temp['BD'] = self.bd
            json.dump(temp, fichero, indent=4)
        fichero.close()
    
    def Notloggued(self):
        if self.dni_ == '' and self.userName_ == '' and self.password_ =='':
            return True
        else:
            return False

    def comprobarUSER(self, u: str, p: str):
        y = []       
        temp = dict()
        temp = self.Usuarios
        for dato in temp:
            y.append(dato['user'])         
        
        for dato in y:
            if (dato[1] == u and dato[2] == p):
                self.datosUsuarioActual(dato[0], dato[1], dato[2])
                break
   
    def showSala(self, roomId: int):       
        devolver = []
        for dato in self.bd:
            if dato['roomId'] == roomId:
                devolver.append({"roomId": dato['roomId'], "capacity": dato['capacity'], 
                                 "Resources": dato['Resources'], "user": dato['user']})
                
                break
        return (devolver)


    def consultaAllSalas(self):
        devolver = []       
        for dato in self.bd:
            devolver.append({"roomId": dato['roomId'], "datosReserva": dato['datosReserva'], "ocupada": dato['ocupada']})
        return (devolver)


    def addBooking(self, roomId: int, date: str, startTime: str, endTime: str):
        duration = 0
                
        hora1 = str(startTime).split(":")
        hora2 = str(endTime).split(":")
        
        t1 = datetime.datetime(1 ,1 ,1 , int(hora1[0]), int(hora1[1]))
        t2 = datetime.datetime(1, 1, 1, int(hora2[0]), int(hora2[1]))
    
        duration = int((t2 - t1).total_seconds() / 60)

        y = []
        salida = []
        cont = 0
        
        # Analizamos si existe la sala
        for dato in self.bd:
            if (dato['roomId']) == roomId:
                y.append(dato['roomId'])
                capacity = dato['capacity']
                Resources = dato['Resources']
                user= dato['user']
                self.room(str(dato['datosReserva'][0]).split('-')) #Almacenaremos el último numero de la Reserva efectuada
    
        nuevaReserva = int(self.Id[1]) + 1
        
        # Si No existe la sala
        if y == []:
            return ({"message": "No existe esa Sala."})
        
        y.clear()
        
        # Analizamos las Reservas llegando hasta la última de la fecha introducida
        for dato in self.bd:
            if (dato['roomId'] == roomId and dato['datosReserva'][2] == date):
                y.append(dato['datosReserva'])
                
        if y == []: 
            opcion = 0 # No hay ninguna reserva en esa fecha
             
        # Comprobamos si no se solapan las horas solicitadas con las existentes de las reservas almacenadas
        h = []
        for dato in y:
            hora1 = str(dato[3]).split(":")
            hora2 = str(dato[5]).split(":")    
            t_start = datetime.datetime(1 ,1 ,1 , int(hora1[0]), int(hora1[1]))
            t_end = datetime.datetime(1, 1, 1, int(hora2[0]), int(hora2[1]))
            if  not (t2 < t_start and t1 < t_start) or (t1 > t_end and t2 > t_end): 
                h.append([hora1, hora2])
        
        if h == []:
            opcion = 1 # las horas No solapan. Añadimos Reserva al final
        else:
            opcion = 2 # las horas se solapan. Imprimiremos aquellas salas con ocupacion
                   
        #return ({"opcion": opcion})

        datosReserva = ([str(roomId) + "-" + str(nuevaReserva) , self.dni_, date, startTime, duration, endTime])                
        
        
        self.contenido(roomId, capacity, Resources, user, datosReserva, 1, "", "")
         
        if (opcion == 0 or opcion == 1):
            self.bd.append({'roomId': self.roomId,
                'capacity': self.capacity,
                'Resources': self.Resources,
                                'user': self.user,
                                'datosReserva': self.datosReserva,
                                'ocupada': self.ocupada,
                                'errorMessage': self.errorMessage,
                                'message': self.message})
            self.guardarJSON()
            return ({"message": "Reserva insertada"})
        
        # Si llegamos hasta aquí entonces es que la reserva se solapa con otras
        # devolveremos todas las salas que cumplan la condición de ocupada = 0
        if (opcion == 2):
            salida = []
            for dato in self.bd:
                if(dato['ocupada'] == 0):
                    salida.append([{"Sala disponible": dato['roomId'], "Resources": dato['Resources']}])
        
            if salida == []:
                return ({"message": "No hay disponibilidad en ninguna sala. Crear nueva sala."})
            else:
                return (salida)

    
    def listaReservas(self, userDNI : str):
        temp = []
        for dato in self.bd:
            if dato['ocupada'] == 1 and dato['datosReserva'][1] == userDNI:
                temp.append({'roomId': dato['roomId'], 'capacity': dato['capacity'], 'Resources': dato['Resources'], 
                             'user': dato['user'], 'datosReserva': dato['datosReserva'], 'ocupada': dato['ocupada'],
                             'errorMessage': dato['errorMessage'], 'message': dato['message']})
        return temp
    
    
    def borrarBooking(self, bookingId: str):
        temp = []
        temp2 = []
        for dato in self.bd:
            if (dato['datosReserva'][0] != bookingId):
                temp.append({'roomId': dato['roomId'], 'capacity': dato['capacity'], 'Resources': dato['Resources'], 
                             'user': dato['user'], 'datosReserva': dato['datosReserva'], 'ocupada': dato['ocupada'],
                             'errorMessage': dato['errorMessage'], 'message': dato['message']})
            else:
                temp2.append({"message": "Reserva Eliminada"})
            
        self.bd = temp
        self.guardarJSON()
            
        if temp2 == []:
            return ({"Error": "50", "message": "No existe ese BookingId."}).encode('utf-8')
        else:
            return ({"message": "Reserva Eliminada."}).encode('utf-8')
    
    
    
#
# FUNCIONES DEL SERVIDOR          
#

h = Reservas()

#Para cargar la Base de Datos desde el CLIENTE
@post('/inicializar')
def cargarBD():
    global h
    
    h.datosUsuarioActual("","","")
    
    try:
        h.cargarJSON()
    except Exception as e:
        return json.dumps({"errorMessage": "99", "message": str(e)}).encode('utf-8')

    return json.dumps({"message": "Base de Datos cargada OK!"}).encode('utf-8')


# Para almacencar la Base de Datos desde el Cliente.
# Se mantiene pero se desactiva temporalmente, pues no lo pide.
#@post('/almacenar')
def guardarBD():
    global h
    
    h.inicioVariables()
    
    try:
        h.guardarJSON()
    except Exception as e:
        return json.dumps({"errorMessage": "98", "message": str(e)}).encode('utf-8')

    return json.dumps({"message": "Base de Datos almacenada OK!"}).encode('utf-8')



#Comprobaremos el nombre de usuario del sistema en la Base de Datos y almacenamos los datos y su DNI
@post('/usuario')
def comprobarusuario():
    global h

    h.datosUsuarioActual("","","")
    h.inicioVariables()

    data = request.json
    userName_ = str(data.get('userName'))
    password_ = str(data.get('password'))
       
    try:
        h.comprobarUSER(userName_, password_)
    except Exception as e:
        return json.dumps({"errorMessage": "97", "message": str(e)}).encode('utf-8')

    if (h.dni_ == ''):
        response.headers['Content-Type'] = 'application/json'
        return json.dumps({"ERROR": 1, "message": "Credenciales no válidas"}).encode('utf-8') 
    else:
        return json.dumps({"ERROR": 0, "DNI": h.dni_, "message": "Usuario logueado correctamente"}).encode('utf-8')


# Añadir una nueva SALA
@post('/addRoom')
def AltaSala():
    global h
    
    h.inicioVariables()
   
    data = request.json
    capacity_ = data.get('capacity')
    Resources_ = data.get('Resources')   
    userName = data.get('userName')
    password = data.get('password')
    response.headers['Content-Type'] = 'application/json'

    # Comprobaremos primero que se ha logueado el cliente.
    if (userName != h.userName_ and password != h.password_ or h.Notloggued()):
        return json.dumps({"errorMessage": "0", "message": "No estas identificado en el sistema"}).encode('utf-8')
    else:        
        try:
            h.insertarsala(capacity_, Resources_)
            h.guardarJSON()
        except Exception as e:
            return json.dumps({"errorMessage": 96, "message": str(e)}).encode('utf-8')

        return json.dumps({"errorMessage": 0, "message": "Sala ( {a} ) creada.".format(a=h.roomId)}).encode('utf-8')


# Mostrar informacion de una SALA concreta.
@post('/showInformationRoom/<roomId>')
def ConsultarSala(roomId: str):
    clave = int(roomId)
    global h
    devolver = []
    data = request.json    
    response.headers['Content-Type'] = 'application/json'
    userName = data.get('userName')
    password = data.get('password')

    # Comprobaremos primero que se ha logueado el cliente.
    if (userName != h.userName_ and password != h.password_ or h.Notloggued()):
        return json.dumps({"errorMessage": "0", "message": "No estas identificado en el sistema"}).encode('utf-8')
    else:           
        h.inicioVariables()
        devolver = h.showSala(clave)

        if h.roomId == []:
            return json.dumps({"ERROR": "La Sala NO existe. Pruebe de nuevo"}).encode('utf-8')
        else:      
            return json.dumps(devolver)
        

# Listar todo el contenido de la BD
@post('/showInformationRoom/all')
def ConsultarAllSalas():
    global h
    devolver = []
    data = request.json    
    
    h.inicioVariables()
    
    response.headers['Content-Type'] = 'application/json'
    userName = data.get('userName')
    password = data.get('password')

    # Comprobaremos primero que se ha logueado el cliente.
    if (userName != h.userName_ and password != h.password_ or h.Notloggued()):
        return json.dumps({"errorMessage": "0", "message": "No estas identificado en el sistema"}).encode('utf-8')
    else:     
        devolver = h.consultaAllSalas()
    
        if devolver == []:
            return json.dumps({"ERROR": "No hay ninguna sala creada. Pruebe de nuevo"}).encode('utf-8')
        else:      
            return json.dumps(devolver).encode('utf-8')
  


# Añadir una nueva RESERVA
@post('/addBooking')
def AltaReserva():
    global h
    data = request.json
    devolver = []
    response.headers['Content-Type'] = 'application/json'    
    
    h.inicioVariables()
    
    roomId = int(data.get('roomId'))
    date = data.get('date')
    startTime = data.get('startTime')
    endTime = data.get('endTime')
    userName = data.get('userName')
    password = data.get('password')

    # Comprobaremos primero que se ha logueado el cliente.
    if (userName != h.userName_ and password != h.password_ or h.Notloggued()):
        return json.dumps({"errorMessage": "0", "message": "No estas identificado en el sistema"}).encode('utf-8')
    else:
        devolver= h.addBooking(roomId, date, startTime, endTime)
    
    return json.dumps(devolver).encode('utf-8')
    

@post('/showBookings/<userDNI>')
def listaReservas(userDNI: str):
    global h
    data = request.json
    response.headers['Content-Type'] = 'application/json'
    devolver = []
    
    h.inicioVariables()
    
    userName = data.get('userName')
    password = data.get('password')

    # Comprobaremos primero que se ha logueado el cliente.
    if (userName != h.userName_ and password != h.password_ or h.Notloggued()):
        return json.dumps({"errorMessage": "0", "message": "No estas identificado en el sistema"}).encode('utf-8')
    else: 
        if not (userDNI.isalnum() and len(userDNI) == 9):
            return json.dumps({"ERROR": "Error al introducir el DNI"}).encode('utf-8')

        devolver = h.listaReservas(userDNI)
                
        if (devolver == []):
            return json.dumps({"ERROR": "El DNI no existe en el sistema"}).encode('utf-8')
        else:
            return json.dumps(devolver).encode('utf-8')
 

@post('/deleteBooking/<bookingId>')
def borrarBooking(bookingId: str):
    global h
    data = request.json
    response.headers['Content-Type'] = 'application/json'
    devolver = []
    
    h.inicioVariables()
    
    userName = data.get('userName')
    password = data.get('password')

    # Comprobaremos primero que se ha logueado el cliente.
    if (userName != h.userName_ and password != h.password_ or h.Notloggued()):
        return json.dumps({"errorMessage": "0", "message": "No estas identificado en el sistema"}).encode('utf-8')
    else: 
        devolver = h.borrarBooking(bookingId)
        return json.dumps(devolver).encode('utf-8')
 


# Se ejecuta el programa
if __name__ == '__main__':
    run(host='localhost', port=8080, debug=True)
    