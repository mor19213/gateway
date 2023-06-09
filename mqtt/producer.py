import paho.mqtt.client as mqtt
from mqtt import producer
import sys
from my_requests import plataformaRequest

# program that every 5 seconds publishes a message to the topic sensor/temperature
# with a random value between 0 and 100
import random
import time

producer = producer()
Request = plataformaRequest("danielam")
while True:
    producer.publish("sensor/temperature", random.randint(0, 100))
    data = {"valor": random.randint(0, 100)}
    print(data)
    Request.put("temperatura", data)
    print(Request.get("luz"))
    time.sleep(5)
