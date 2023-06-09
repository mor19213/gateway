import paho.mqtt.client as mqtt
import json
from mqtt import producer

producer = producer()

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # subscribe to all topics starting with sensors/
    client.subscribe("sensor/#")

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    payload = json.loads(msg.payload)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect('localhost', 1883, 60)
client.loop_forever()