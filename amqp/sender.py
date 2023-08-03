import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='192.168.0.122'))
channel = connection.channel()

channel.queue_declare(queue='hello')

channel.basic_publish(exchange='', routing_key='hello', body='Hello World!')
print(" [x] Sent 'Hello World!'")
connection.close()