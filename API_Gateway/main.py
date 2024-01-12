from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
import requests
from fastapi.encoders import jsonable_encoder
import os
import json

class usuario():
    def __init__(self, username: str, password: str, access: str, refresh: str):
        self.username = username
        self.password = password
        self.access = access
        self.refresh = refresh
        self.sensores = {}


app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
u = usuario("mor19213", "Tesis123$", "", "")
base_url = "https://backend-tesis-mor19213.cloud.okteto.net"
hist_url = "https://historical-tesis-mor19213.cloud.okteto.net"

@app.get("/{user}/login")
def login(user: str):
    
    data = {"username": user, "password": u.password}
    response = requests.post(base_url + "/tokens", data)
    if response.status_code != 200:
        raise HTTPException(status_code=401, detail="Could not authenticate")
    
    u.access = response.json()["access"]
    u.refresh = response.json()["refresh"]
    u.access_h = None
    u.refresh_h = None
    return None

login("mor19213")

def refresh(refresh: str):
    data = {"refresh": u.refresh}
    response = requests.post(base_url + "/tokens/refresh", data)
    u.access = response.json()["access"]
    u.refresh = response.json()["refresh"]
    if response.status_code != 200:
        u.access, u.refresh = login(u.username)
        if u.access is None:
            return None, None
    return access_token, refresh_token

@app.get("/{user}/actuadores/{nombre}")
def get_endpoint(user:str, nombre: str):
    print(f"{u.access=}")
    if u.access is None:
        u.access, u.refresh = login(u.username)
    response = requests.get(
        f"{base_url}/{user}/actuadores/{nombre}", headers={"Authorization": "Bearer " + u.access})
    print(f"{response}")
    if response.status_code == 403:
        u.access, u.refresh = refresh(u.refresh)
        if u.access is None:
            exit()
        response = requests.get(
            f"{base_url}/{user}/actuadores/{nombre}", headers={"Authorization": "Bearer " + u.access})
    return JSONResponse(status_code=response.status_code, content=jsonable_encoder(response.json()))

@app.put("/{user}/sensores/{nombre}")
def put_endpoint(user:str, nombre: str, data: dict):
    response = requests.put(
        f"{base_url}/{user}/sensores/{nombre}", json=data, headers={"Authorization": f"Bearer " + u.access})
    if response.status_code == 403:
        u.access, u.refresh = refresh(u.refresh)
        if u.access is None:
            exit()
        response = requests.put(
            f"{base_url}/{user}/sensores/{nombre}", json=data, headers={"Authorization": f"Bearer " + u.access})
    update_historical(nombre, data, user)
    return JSONResponse(status_code=response.status_code, content=jsonable_encoder({"status": "ok"}))

def update_historical(nombre: str, sens_data: dict, user: str):
    response = None
    url = f"{hist_url}/users/{user}/sensor/{nombre}/valores/{sens_data['valor']}"
    print(url)
    valor = u.sensores.get(nombre)
    if valor is None:
        u.sensores[nombre] = 0
        valor = 0
    u.sensores[nombre] += 1
    if valor == 0:
        if u.access_h is None:
            # login a histórico
            
            data = {"username": user, "password": u.password}
            print("request a login")
            response = requests.post(hist_url + "/login", json=json.dumps(data))
            print(response.status_code)
            print(response.json())
            if response.status_code in [403, 422]:
                print("No se pudo autenticar en el historiador")
                return None
            u.access_h = response.json()["access_token"]
            u.refresh_h = response.json()["refresh_token"]
        response = requests.post(url+"?access_token="+str(u.access_h))
        print("request a subir data 1")
        if response.status_code == 403:
            response = requests.post(hist_url+"/refresh?refresh="+ str(u.refresh_h))
            print("request a refresar")
            if response.status_code == 401:
                print("No se pudo refrescar el token")
                return None
            u.access_h = response.json()["access_token"]
            u.refresh_h = response.json()["refresh_token"]
            response = requests.post(url+"?access_token="+str(u.access_h))
            print("request a subir data 2")
        
    elif valor > 100:
        u.sensores[nombre] = 0
    print(u.sensores)
    return None

@app.get("/{user}/dispositivos")
def get_dispositivos(user: str):
    response = requests.get(f"{base_url}/{user}")
    if response.status_code == 403:
        u.access, u.refresh = refresh(u.refresh)
        if u.access is None:
            exit()
        response = requests.get(f"{base_url}/{user}")
    return JSONResponse(status_code=response.status_code, content=response.json())