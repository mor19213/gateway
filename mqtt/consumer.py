import paho.mqtt.client as mqtt
import json
from mqtt import producer
from my_requests import plataformaRequest

producer = producer()
Request = plataformaRequest("danielam")

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("sensor/#")

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    name = (msg.topic.split("/")[1])
    tipo = (msg.topic.split("/")[0])
    if tipo == "sensor":
        try:
            print("nombre del sensor: "+name)
            payload = json.loads(msg.payload)
            print("valor del sensor: "+str(payload))
            data = {"valor": payload}
            print(data)
            status = Request.put(name, data)
            if status == 200:
                print("actualizado")
            else:
                print("error")
        except:
            print("formato distinto al esperado")
            print(msg.payload)
    else:
        print("tipo incorrecto")


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect('localhost', 1883, 60)
client.loop_forever()