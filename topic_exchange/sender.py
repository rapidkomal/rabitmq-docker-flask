from flask import Flask, request
import pika
app = Flask(__name__)

def publish_to_queue(message):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    #  Create ExchangeA and ExchangeB
    channel.exchange_declare(exchange='TopicExchangeA', exchange_type='topic')
    channel.exchange_declare(exchange='TopicExchangeB', exchange_type='topic')
    
    # Create TopicQueueA and TopicQueueB
    channel.queue_declare(queue='TopicQueueA')
    channel.queue_declare(queue='TopicQueueB')

    
    # Bind QueueA to ExchangeA with the routing key "mykey"
    channel.queue_bind(queue='TopicQueueA', exchange='TopicExchangeA', routing_key='topic.com')


    # Publish a message to ExchangeA with the routing key "mykey"
    channel.basic_publish(exchange='TopicExchangeA', routing_key='topic.com', body='Hello from ExchangeA!')

    connection.close()

@app.route('/messages', methods=['GET'])
def send_message():
    # message = input("please enter the message to publish: ")
    message = "hello"
    for i in range(100):
        print(str(i))
        publish_to_queue(str(i))
    return 'Message sent to queue!'

if __name__ == "__main__":
    app.run(debug=True)
    