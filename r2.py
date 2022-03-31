# Receptor (consumidor)

import pika


def callback(ch, method, properties, body):
    print('[x] Received %r' % body)
    # Envíe un mensaje a la cola para confirmar la ejecución;
    # de lo contrario, el mensaje se guardará, no se consumirá
    # y se transferirá al siguiente consumidor.
    ch.basic_ack(delivery_tag=method.delivery_tag)

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Aquí nuevamente declara que para recibir mensajes de esa cola
# (puede dejarlo, pero debe tener esta cola, o recibirá un error)
q = channel.queue_declare(queue='hello') # Durable = Verdadero Persistencia para la cola
channel.basic_qos(prefetch_count=1)

channel.basic_consume(queue='hello', on_message_callback=callback) # No_ack = True # Cancele la función de
# procesamiento de interrupción de envío de mensajes, no importa si se ha procesado,
# no enviará una confirmación al servidor.

mensajes = q.method.message_count
print("Numero de mensajes pendientes en la cola: " + str(mensajes))
print('[*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
