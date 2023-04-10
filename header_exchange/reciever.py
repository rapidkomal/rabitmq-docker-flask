import threading
from flask import Flask, request
import pika

def consume_from_queue():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
   
    # Declare the header exchange
    channel.exchange_declare(exchange='HeaderExchange', exchange_type='headers')

    # Declare the queues
    channel.queue_declare(queue='HeaderQueueA')
    channel.queue_declare(queue='HeaderQueueB')

    # Bind the queues to the exchange with headers
    channel.queue_bind(queue='HeaderQueueA', exchange='HeaderExchange', arguments={'x-match': 'all', 'key1': 'value1'})
    channel.queue_bind(queue='HeaderQueueB', exchange='HeaderExchange', arguments={'x-match': 'any', 'key1': 'value1', 'key2': 'value2'})

    channel.basic_consume(queue='HeaderQueueA', on_message_callback=process_message, auto_ack=True)
    channel.basic_consume(queue='HeaderQueueB', on_message_callback=process_message, auto_ack=True)
     
    channel.start_consuming()

def process_message(channel, method, properties, body):
    print("Received message: %s" % body.decode())
     

t = threading.Thread(target=consume_from_queue)
t.start()
 