from flask import Flask, request
import pika
app = Flask(__name__)

def publish_to_queue(message):
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

    # Publish messages with headers
    channel.basic_publish(exchange='HeaderExchange', routing_key='', body='Message 1', properties=pika.BasicProperties(headers={'key1': 'value1'}))
    channel.basic_publish(exchange='HeaderExchange', routing_key='', body='Message 2', properties=pika.BasicProperties(headers={'key1': 'value1', 'key2': 'value2'}))
    channel.basic_publish(exchange='HeaderExchange', routing_key='', body='Message 3', properties=pika.BasicProperties(headers={'key2': 'value2'}))

    connection.close()

@app.route('/messages', methods=['GET'])
def send_message():
    # message = input("please enter the message to publish: ")
    message = "hello"
    for i in range(10):
        print(str(i))
        publish_to_queue(str(i))
    return 'Message sent to queue!'

if __name__ == "__main__":
    app.run(debug=True)
    