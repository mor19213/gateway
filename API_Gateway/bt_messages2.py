import bluetooth
import threading
import time
import select
import sys
import queue
import requests

# Create a queue for input
input_queue = queue.Queue()
exit_flag = False
logs = True
active_reconnect = True
username = "mor19213"
url = f"http://192.168.0.122:8000/{username}"
def scan():
    print("Scanning for Bluetooth devices:")
    devices = bluetooth.discover_devices(lookup_names=True, lookup_class=True)
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
                received = data.decode('utf-8')
                if "sensor" in received:
                    parts = received.split("/")
                    if len(parts) >= 3:
                        nombre, valor = parts[1], parts[2].split("\n")[0]
                        try:
                            valor = float(valor)
                            data = {"valor": str(valor)}
                        except ValueError:
                            continue
                        if logs:
                            print(f"{nombre}: {data}")
                        my_request = requests.put(f"{url}/sensores/{nombre}", json=data)
                        #my_request = Request.put(nombre, data)
                elif "actuador" in received:
                    parts = received.split("/")
                    if len(parts) >= 2:
                        nombre = parts[1].split("\n")[0]
                        if nombre == "actuador":
                            continue
                        my_request = requests.get(f"{url}/actuadores/{nombre}")
                        #my_request = Request.get(nombre)
                        if my_request.status_code == 200:
                            data = str({'valor': str(my_request.json()["valor"])})
                            if logs:
                                print(f"{nombre}: {data}")
                            sock.send(data.encode('utf-8'))
                        else:
                            print("Error in request")
                elif "desconectar" in received:
                    if logs:
                        print("Disconnected")
                    sock.close()
                    exit_flag = True
                    return
            except bluetooth.btcommon.BluetoothError as e:
                if logs:
                    print(f"Bluetooth error {name}: {e}")
                sock.close()
                exit_flag = True
                return
    except Exception as e:
        if logs:
            print(f"Error: {e}")
        sock.close()
        exit_flag = True

cmd = ""
ejecutando = True

def reconectar_todos():
    global exit_flag
    global logs
    global active_reconnect
    global cmd
    global ejecutando

    hilos, puerto = conectar(1)
    while ejecutando:
        cmd = ""
        while not hilos and active_reconnect:
            hilos, puerto = conectar(puerto)
            time.sleep(5)
        try:
            rlist, _, _ = select.select([sys.stdin], [], [], 0.1)  # Check for input every 0.1 seconds
            if rlist:
                cmd = sys.stdin.readline().strip().lower()
        except Exception:
            pass

        if cmd in ["1", "l", "logs"]:
            logs = not logs  # Toggle logs
            print(f'Logs estan {"habilitados" if logs else "desabilitados"}.')
        elif cmd in ["2", "r", "reconectar"]:
            exit_flag = True
            for h in hilos:
                h.join()  # Wait for threads to finish
            print("Se han desconectado todos los dispositivos")
            exit_flag = False
            time.sleep(5)
            hilos, puerto = conectar(puerto)
        elif cmd in ["3", "q", "quit", "exit"]:
            exit_flag = True
            for h in hilos:
                h.join()  # Wait for threads to finish
            exit_flag = False
            ejecutando = False
            print("El programa ha terminado")

def conectar(puerto):
    dispositivos = scan()
    print(dispositivos)
    hilos = []
    for addr, name, device_class in dispositivos:
        if "Disp" in name:
            print(name)
            sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            sock.connect((addr, 1))
            hilo = threading.Thread(target=device, args=(name, sock, puerto))
            hilo.start()
            hilos.append(hilo)
            puerto += 1
    return hilos, puerto

general = threading.Thread(target=reconectar_todos)
general.daemon = True
general.start()

while ejecutando:
    try:
        user_input = input_queue.get(block=False)  # Check for input in the queue
        print(f"Received input: {user_input}")
    except queue.Empty:
        pass
