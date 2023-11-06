import requests
import os

class plataformaRequest:
    def __init__(self, user):
        self.base_url = "https://backend-tesis-mor19213.cloud.okteto.net/"
        self.url = "https://backend-tesis-mor19213.cloud.okteto.net/"+user
        self.access = ""
        self.refresh = ""
        self.username = user
        self.password = os.environ.get('PASSWORD')
        if self.password is None:
            raise Exception("PASSWORD environment variable not set")
        response = self.login()
    
    def login(self):
        data = {"username": self.username, "password": self.password}
        response = requests.post(self.base_url + "/tokens", data)
        if response.status_code != 200:
            raise Exception("No se pudo iniciar sesion")
        self.access = response.json()["access"]
        self.refresh = response.json()["refresh"]
        return response

    def refresh_token(self):
        data = {"refresh": self.refresh, "username": self.username}
        response = requests.post(self.base_url + "/tokens/refresh", {"data": data})
        self.access = response.json()["access"]
        return response

    def get(self, nombre):
        response = requests.get(self.url +"/actuadores/"+ nombre, headers={"Authorization": "Bearer " + self.access})
        if response.status_code == 403:
            self.login()
            response = requests.get(self.url +"/actuadores/"+ nombre, headers={"Authorization": "Bearer " + self.access})
        return response

    def put(self, nombre, data):
        #print(self.url + "/sensor/"+ nombre)
        response = requests.put(self.url+"/sensores/" + nombre, json=data, headers={"Authorization": "Bearer " + self.access})
        if response.status_code == 403:
            self.login()
            response = requests.put(self.url+"/sensores/" + nombre, json=data, headers={"Authorization": "Bearer " + self.access})
        return response
    
    def get_dispositivos(self):
        response = requests.get(self.url)
        return response

    def put_dev(self, nombre, data):
        #print("http://127.0.0.1:8000/mor19213/sensor/"+ nombre)
        response = requests.put("http://127.0.0.1:8000/mor19213/sensores/"+ nombre, json=data)
        return response