# Envio (Productor)
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()  # declara un canal

# En la tubería, luego declarar la cola
channel.queue_declare(queue='hello') # Durable = Verdadero Persistencia para la cola

# Mensaje de envío verdadero, envío por tubería
channel.basic_publish(exchange='', routing_key='hello',  # nombre de la cola de mensajes
                      body = 'Hello World!') # pika.BasicProperties (delivery_mode = 2,) message persistence

print('[x] sent "Hello World!"')
connection.close()
