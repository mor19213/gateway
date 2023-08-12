import bluetooth
import threading

def scan():
    print("Scanning for bluetooth devices:")
    devices = bluetooth.discover_devices(lookup_names = True, lookup_class = True)
    return devices

dispositivos = scan()
print(dispositivos)

def device(name, puerto):
    print("init")
    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    sock.connect((addr, puerto))
    message = "C"
    sock.send("{}".format(message))
    while True:
        # check if the bluetooth connection is still open
        if sock.fileno() == -1:
            print("esperando data")
            data = sock.recv(2048)
            if not data:
                break
            recibido = data.decode('utf-8')
            print(f"Recibido: {recibido}")
            if recibido.find("sensor") != -1:
                nombre = recibido.split("/")[1]
                valor = recibido.split("/")[2]
                print("nombre: {nombre}, valor: {valor}}")
            elif recibido.find("actuador") != -1:
                nombre = recibido.split("/")[1]
                print("nombre: {nombre}")
            elif recibido.find("desconectar") != -1:
                print("desconectar dispositivo {name}")
                return
        else:
            sock.close()
            return
    sock.close()
    return

puerto = 1
for addr, name, device_class in dispositivos:
    if name.find("Disp") != -1:
        print(name)
        threading.Thread(target=device, args=(name, puerto)).start()
        puerto += 1