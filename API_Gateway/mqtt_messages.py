import paho.mqtt.client as mqtt
import json
from mqtt import producer
import requests
import sys
sys.path.append("..")
producer = producer()
username = "mor19213"
url = f"http://127.0.0.1:8000/{username}"
#resp = requests.get(f"{url}/login")

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("sensor/#")
    client.subscribe("actualizar/")

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    name = (msg.topic.split("/")[1])
    tipo = (msg.topic.split("/")[0])
    if tipo == "sensor":
        payload = json.loads(msg.payload)   
        payload["valor"] = str(payload["valor"])
        if payload["valor"]:
            try:
                #print("nombre del sensor: "+name)
                data = payload
                print(f"data: {data}")
                my_request = requests.put(f"{url}/sensores/{name}", json=data)
                if my_request.status_code == 200:
                    print("actualizado")
                else:
                    print(my_request)
            except:
                e = input("salir: ")
                if e=="Y":
                    exit()
                print("formato distinto al esperado")
                print(msg.payload)
        else:
            print("No se envio el valor del sensor")
    elif tipo == "actualizar":
        print("tipo actualizar")
        payload = msg.payload.decode('utf-8')
        name = payload
        
        my_request = requests.get(f"{url}/actuadores/{name}")
        if my_request.status_code == 200:
            data = my_request.json()
            data = str({'valor': str(data["valor"])})
            print(data)
            producer.publish("actuador/"+str(name), data)

        else:
            print(my_request)

    else:
        print("tipo incorrecto")


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect('localhost', 1883, 60)
client.loop_forever()