# rabitmq-docker-flask
#### Rabbit Mq 
RabbitMQ is an open-source message broker software that enables different software applications to communicate and exchange data with each other in a distributed computing environment. It is based on the Advanced Message Queuing Protocol (AMQP), which is a widely accepted standard for message-oriented middleware.

##### Type of exchange 
1.Direct exchange: This exchange delivers messages to queues based on a direct match between the routing key of the message and the binding key of the queue.

2.Fanout exchange: This exchange delivers messages to all the queues that are bound to it, regardless of the routing key.

3.Topic exchange: This exchange delivers messages to queues based on wildcard patterns that match the routing key of the message.

4.Headers exchange: This exchange delivers messages to queues based on header values that match the headers of the message.

#### Flask 
Flask is a lightweight web application framework for Python that allows developers to quickly build web applications. It is based on the WSGI (Web Server Gateway Interface) toolkit and is designed to be easy to use and to have a low learning curve.

### Installation 

##### venv env
```python3 -m venv venv```

##### Activate Env
```source venv/bin/activate```

##### Install pika and flask
```pip install pika flask```

### To Run Direct, Fanout, Topic and Header Exchange
##### sender.py in one terminal
```python direct_exchange/sender.py```

##### receiver.py in another terminal to see the message 
```python direct_exchange/reciever.py```
