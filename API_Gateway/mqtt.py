import paho.mqtt.client as mqtt

class producer:
    def __init__(self):
        self.producer = mqtt.Client()
        self.producer.connect("localhost", 1883, 60)

    def publish(self, topic, message):
        self.producer.publish(topic, message)

class consumer:
    def __init__(self, topic):
        self.consumer = mqtt.Client()
        self.consumer.on_connect = self.on_connect
        self.consumer.on_message = self.on_message
        self.consumer.connect("localhost", 1883, 60)
        self.consumer.subscribe(topic)
        self.consumer.loop_forever()

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))

    def on_message(self, client, userdata, msg):
        print(msg.topic+" "+str(msg.payload))
