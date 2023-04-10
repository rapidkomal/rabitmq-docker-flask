import threading
from flask import Flask, request
import pika

def consume_from_queue():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
   
    # Create ExchangeA and ExchangeD
    channel.exchange_declare(exchange='FanoutExchangeA', exchange_type='fanout')

    # Create QueueA and QueueB
    channel.queue_declare(queue='FanoutQueueA')
    channel.queue_declare(queue='FanoutQueueB')
    # Unbind the exchange "ExchangeA" from the queue "QueueB"
    # channel.queue_unbind(queue='QueueD', exchange='ExchangeA', routing_key='mykey2')

    # Bind QueueB to ExchangeD with the same routing key "mykey"
    channel.queue_bind(queue='FanoutQueueA', exchange='FanoutExchangeA', routing_key='')
    channel.queue_bind(queue='FanoutQueueB', exchange='FanoutExchangeA', routing_key='')

    channel.basic_consume(queue='FanoutQueueA', on_message_callback=process_message, auto_ack=False)
    channel.basic_consume(queue='FanoutQueueB', on_message_callback=process_message, auto_ack=False)
    channel.start_consuming()

def process_message(channel, method, properties, body):
    print("Received message: %s" % body.decode())
    channel.basic_ack(delivery_tag=method.delivery_tag)
 

t = threading.Thread(target=consume_from_queue)
t.start()