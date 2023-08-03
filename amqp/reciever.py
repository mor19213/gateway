import pika, sys, os

def main():
    credentials = pika.PlainCredentials('passwordless-user', '')  # Provide the username and empty password
    host = input("Enter the IP address of the RabbitMQ server: ")
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))#'192.168.0.122'))
    channel = connection.channel()

    # Declare an empty queue with auto-generated name
    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue

    # Bind the queue to all available queues using the wildcard character '#'
    channel.queue_bind(exchange='amq.direct', queue=queue_name, routing_key='#')

    def callback(ch, method, properties, body):
        print(f" [x] Received {body}")

    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
