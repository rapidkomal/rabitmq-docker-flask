from flask import Flask, request
import pika
app = Flask(__name__)

def publish_to_queue(message):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    #  Create ExchangeA and ExchangeB
    channel.exchange_declare(exchange='FanoutExchangeA', exchange_type='fanout')
    channel.exchange_declare(exchange='FanoutExchangeB', exchange_type='fanout')
    
    # Create TopicQueueA and TopicQueueB
    channel.queue_declare(queue='FanoutQueueA')
    channel.queue_declare(queue='FanoutQueueB')

    
    # Bind QueueA to ExchangeA with the routing key "mykey"
    channel.queue_bind(queue='FanoutQueueA', exchange='FanoutExchangeA', routing_key='')
    channel.queue_bind(queue='FanoutQueueB', exchange='FanoutExchangeB', routing_key='test')

    # Publish a message to ExchangeA with the routing key "mykey"
    channel.basic_publish(exchange='FanoutExchangeA', routing_key='', body='Hello from FanoutExchangeA!')
    channel.basic_publish(exchange='FanoutExchangeB', routing_key='test', body='Hello from FanoutExchangeB!')

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
    