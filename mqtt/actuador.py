import paho.mqtt.client as mqtt
import json
from mqtt import producer
from my_requests import plataformaRequest

producer = producer()
Request = plataformaRequest("mor19213")

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("actualizar/")

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    name = (msg.topic.split("/")[1])
    tipo = (msg.topic.split("/")[0])
    if tipo == "actualizar":
        print("tipo actualizar")
        payload = msg.payload.decode('utf-8')
        name = payload
        print(name)
        my_request = Request.get(name)
        if my_request.status_code == 200:
            data = my_request.json()
            data = str({'valor': str(data["valor"])})
            print(data)
            producer.publish("actuador/"+name, data)

        else:
            print(my_request)

    else:
        print("tipo incorrecto")


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect('localhost', 1883, 60)
client.loop_forever()