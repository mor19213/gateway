import requests

class plataformaRequest:
    def __init__(self, user):
        self.url = "https://backend-tesis-mor19213.cloud.okteto.net/"+user

    def get(self, nombre):
        response = requests.get(self.url +"/actuador/"+ nombre)
        #print(self.url +"/actuador/"+ nombre)
        return response

    def put(self, nombre, data):
        #print(self.url + "/sensor/"+ nombre)
        response = requests.put(self.url+"/sensor/" + nombre, json=data)
        return response
    
    def get_dispositivos(self):
        response = requests.get(self.url)
        return response

    def put_dev(self, nombre, data):
        #print("http://127.0.0.1:8000/mor19213/sensor/"+ nombre)
        response = requests.put("http://127.0.0.1:8000/mor19213/sensor/"+ nombre, json=data)
        return response