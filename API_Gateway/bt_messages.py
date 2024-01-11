import bluetooth
import threading
import time
import requests
import json

username = "mor19213"
url = f"http://127.0.0.1:8000/{username}"
resp = requests.get(f"{url}/login")
exit_flag = False
logs = True

def scan():
    print("Scanning for bluetooth devices:")
    devices = bluetooth.discover_devices(lookup_names = True, lookup_class = True)
    return devices

def device(name, sock, puerto):
    global exit_flag
    global logs
    print(f"Connected to {name}")
    try:
        while sock.fileno() != -1 and not exit_flag:
            try:
                data = sock.recv(2048)
                if not data:
                    break
                recibido = data.decode('utf-8')
                if recibido.find("sensor") != -1:
                    nombre = recibido.split("/")[1]
                    valor = recibido.split("/")[2]
                    valor = valor.split("\n")[0]
                    try:
                        valor = float(valor)
                        data = {"valor": str(valor)}
                    except:
                        continue
                    if logs:
                        print(nombre +": "+str(data))
                    #my_request = Request.put(nombre, data)
                    my_request = requests.put(f"{url}/sensores/{nombre}", json=data)
                elif recibido.find("actuador") != -1:
                    nombre = recibido.split("/")[1]
                    nombre = nombre.split("\n")[0]
                    if nombre == "actuador":
                        continue
                    my_request = requests.get(f"{url}/actuadores/{nombre}")
                    #my_request = Request.get(nombre)
                    if my_request.status_code == 200:
                        data = my_request.json()
                        data = str({'valor': str(data["valor"])})
                        if logs:
                            print(nombre +": "+str(data))
                        sock.send("{}".format(data))
                    else:
                        print("Error en request")
                elif recibido.find("desconectar") != -1:
                    if logs:
                        print("Desconectado")
                    sock.close()
                    return
            except bluetooth.btcommon.BluetoothError as e:
                if logs:
                    print(f"Bluetooth error {name}: {e}")
                sock.close()
                return
    except Exception as e:
        #print(f"Error: {e}")
        sock.close()
        return

def reconectar_todos():
    global exit_flag
    global logs
    ejecutando = True
    hilos, puerto = conectar(1)
    while ejecutando:
        cmd = input("").lower()        
        if cmd in ["1", "l", "logs"]:
            logs = not logs     # Toggle logs
            print(f'Logs are {"enabled" if logs else "disabled"}.')
        elif cmd in ["2", "r", "reconectar"]:
            exit_flag = True
            for h in hilos:
                h.join()    # Esperar a que los hilos terminen de ejecutarse
            print("Se han desconectado todos los dispositivos")
            exit_flag = False
            time.sleep(5)
            hilos = []
            hilos, puerto = conectar(puerto)
        elif cmd in ["3", "q", "quit", "exit"]:
            exit_flag = True
            for h in hilos:
                h.join()    # Esperar a que los hilos terminen de ejecutarse
            exit_flag = False
            ejecutando = False


def conectar(puerto):
    dispositivos = scan()
    print(dispositivos)
    hilos = []
    for addr, name, device_class in dispositivos:
        if name.find("Disp") != -1:
            print(name)
            sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            sock.connect((addr, 1))
            #device(name, sock, puerto)
            hilo = threading.Thread(target=device, args=(name, sock, puerto))
            hilo.start()
            hilos.append(hilo)
            puerto += 1
    return hilos, puerto

threading.Thread(target=reconectar_todos, args=()).start()