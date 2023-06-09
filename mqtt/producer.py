import time
import paho.mqtt.client as mqtt
import json
from mqtt import producer
from my_requests import plataformaRequest

producer = producer()
Request = plataformaRequest("danielam")
name = "luz"
print("inicio")

while True:
    data = json.loads(Request.get(name).text)
    #print(Request.get(name))
    #print(type(data))
    producer.publish("actuador/"+name, data["valor"])
    print(data)

    time.sleep(5)
