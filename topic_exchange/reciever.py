import threading
from flask import Flask, request
import pika

def consume_from_queue():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
   
     # Create TopicExchangeA and ExchangeB
    channel.exchange_delete(exchange='TopicExchangeA')

    # Create TopicExchangeA and ExchangeB
    channel.exchange_declare(exchange='TopicExchangeA', exchange_type='topic')

    # Create TopicQueueA and QueueB
    channel.queue_declare(queue='TopicQueueA')
    
     # Bind TopicQueueA to TopicExchangeA with the routing key "mykey"
    channel.queue_bind(queue='TopicQueueA', exchange='TopicExchangeA', routing_key='topic.*')


    channel.basic_consume(queue='TopicQueueA', on_message_callback=process_message, auto_ack=True)
    channel.start_consuming()

def process_message(channel, method, properties, body):
    print("Received message: %s" % body.decode())
     

t = threading.Thread(target=consume_from_queue)
t.start()
 