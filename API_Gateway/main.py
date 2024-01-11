from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
import requests
from fastapi.encoders import jsonable_encoder
import os

class usuario():
    def __init__(self, username: str, password: str, access: str, refresh: str):
        self.username = username
        self.password = password
        self.access = access
        self.refresh = refresh

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
u = usuario("mor19213", "Tesis123$", "", "")
base_url = "https://backend-tesis-mor19213.cloud.okteto.net"
hist_url = "https://historical-tesis-mor19213.cloud.okteto.net"

@app.get("/{user}/login")
def login(user: str):
    data = {"username": user, "password": u.password}
    response = requests.post(base_url + "/tokens", data)
    u.access = response.json()["access"]
    u.refresh = response.json()["refresh"]
    if response.status_code != 200:
        raise HTTPException(status_code=401, detail="Could not authenticate")
    return JSONResponse(status_code=200, content="Logged in")


def refresh(refresh: str):
    data = {"refresh": refresh}
    response = requests.post(base_url + "/tokens/refresh", data)
    u.access = response.json()["access"]
    u.refresh = response.json()["refresh"]
    if response.status_code != 200:
        raise HTTPException(status_code=401, detail="Could not authenticate")
    return access_token, refresh_token

@app.get("/{user}/actuadores/{nombre}")
def get_endpoint(user:str, nombre: str):
    print(f"{u.access=}")
    response = requests.get(
        f"{base_url}/{user}/actuadores/{nombre}", headers={"Authorization": "Bearer " + u.access})
    print(f"{response}")
    if response.status_code == 403:
        u.access, u.refresh = refresh(u.refresh)
        response = requests.get(
            f"{base_url}/{user}/actuadores/{nombre}", headers={"Authorization": "Bearer " + u.access})
    return JSONResponse(status_code=response.status_code, content=jsonable_encoder(response.json()))

@app.put("/{user}/sensores/{nombre}")
def put_endpoint(user:str, nombre: str, data: dict):
    response = requests.put(
        f"{base_url}/{user}/sensores/{nombre}", json=data, headers={"Authorization": f"Bearer " + u.access})
    if response.status_code == 403:
        u.access, u.refresh = refresh(refresh)
        response = requests.put(
            f"{base_url}/{user}/sensores/{nombre}", json=data, headers={"Authorization": f"Bearer " + u.access})
    update_historical(nombre, data, user)
    return JSONResponse(status_code=response.status_code, content=jsonable_encoder({"status": "ok"}))

def update_historical(nombre: str, data: dict, user: str):
    response = None
    counter = 0
    if counter == 0:
        response = requests.post(
            f"{hist_url}/users/{user}/sensor/{nombre}/valores/{data['valor']}")
    elif counter == 100:
        counter = 0
    counter += 1
    return None

@app.get("/{user}/dispositivos")
def get_dispositivos(user: str):
    response = requests.get(f"{base_url}/{user}")
    if response.status_code == 403:
        u.access, u.refresh = refresh(u.refresh)
        response = requests.get(f"{base_url}/{user}")
    return JSONResponse(status_code=response.status_code, content=response.json())