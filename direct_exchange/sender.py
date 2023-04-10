from flask import Flask, request
import pika
app = Flask(__name__)

def publish_to_queue(message):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    #  Create DirectExchangeA and DirectExchangeB
    channel.exchange_declare(exchange='DirectExchangeA', exchange_type='direct')
    channel.exchange_declare(exchange='DirectExchangeB', exchange_type='direct')
    
  
    # Create DirectQueueA and DirectQueueB
    channel.queue_declare(queue='DirectQueueA')
    channel.queue_declare(queue='DirectQueueB')
    
    # Bind QueueA to ExchangeA with the routing key "mykey"
    channel.queue_bind(queue='DirectQueueA', exchange='DirectExchangeA', routing_key='mykey')

    # Bind QueueB to ExchangeB with the same routing key "mykey"
    channel.queue_bind(queue='DirectQueueB', exchange='DirectExchangeB', routing_key='mykey')

    # Publish a message to ExchangeA with the routing key "mykey"
    channel.basic_publish(exchange='DirectExchangeA', routing_key='mykey', body='Hello from ExchangeA!')

    # Publish a message to ExchangeB with the routing key "mykey"
    channel.basic_publish(exchange='DirectExchangeB', routing_key='mykey', body='Hello from ExchangeB!')
    
    connection.close()

@app.route('/messages', methods=['GET'])
def send_message():
    # message = input("please enter the message to publish: ")
    message = "hello"
    for i in range(100):
        publish_to_queue(str(i))
    return 'Message sent to queue!'

if __name__ == "__main__":
    app.run(debug=True)
    