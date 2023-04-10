import threading
from flask import Flask, request
import pika

def consume_from_queue():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
   
    # Create DirectExchangeB
    channel.exchange_declare(exchange='DirectExchangeA', exchange_type='direct')

    # CreateDirectQueueB
    channel.queue_declare(queue='DirectQueueA')

    # Unbind the exchange "DirectExchangeA" from the queue "DirectQueueB"
    # channel.queue_unbind(queue='DirectQueueA', exchange='DirectExchangeA', routing_key='mykey')

    # Bind QueueB to DirectExchangeA with the same routing key "mykey"
    channel.queue_bind(queue='DirectQueueA', exchange='DirectExchangeA', routing_key='mykey')

    channel.basic_consume(queue='DirectQueueA', on_message_callback=process_message, auto_ack=False)
    channel.start_consuming()

def process_message(channel, method, properties, body):
    print("Received message: %s" % body.decode())
    channel.basic_ack(delivery_tag=method.delivery_tag)
 

t = threading.Thread(target=consume_from_queue)
t.start()