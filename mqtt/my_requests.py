import requests

class plataformaRequest:
    def __init__(self, user):
        self.url = "https://backend-tesis-profolio-gt.cloud.okteto.net/dispositivos/"+user

    def get(self, nombre):
        response = requests.get(self.url +"/"+ nombre)
        print(self.url +"/"+ nombre)
        return response

    def put(self, nombre, data):
        print(self.url + nombre)
        response = requests.put(self.url+"/" + nombre, json=data)
        return response.status_code
    
    def get_dispositivos(self):
        response = requests.get(self.url)
        return response