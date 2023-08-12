import bluetooth
import threading

def scan():
    print("Scanning for bluetooth devices:")
    devices = bluetooth.discover_devices(lookup_names = True, lookup_class = True)
    return devices

dispositivos = scan()
print(dispositivos)

def device(name, sock, puerto):
    try:
        while sock.fileno() != -1:
            try:
                data = sock.recv(2048)
                if not data:
                    break
                recibido = data.decode('utf-8')
                print(f"Recibido: {recibido}")
                if recibido.find("sensor") != -1:
                    nombre = recibido.split("/")[1]
                    valor = recibido.split("/")[2]
                elif recibido.find("actuador") != -1:
                    nombre = recibido.split("/")[1]
                elif recibido.find("desconectar") != -1:
                    print("Desconectado")
                    sock.close()
                    return
            except bluetooth.btcommon.BluetoothError as e:
                print(f"Bluetooth error: {e}")
                print("Desconectado")
                sock.close()
                return
    except Exception as e:
        print(f"Error: {e}")
        sock.close()
        return
    
puerto = 1
for addr, name, device_class in dispositivos:
    if name.find("Disp") != -1:
        print(name)
        sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        sock.connect((addr, 1))
        message = "C"
        sock.send("{}".format(message))
        #device(name, sock, puerto)
        threading.Thread(target=device, args=(name, sock, puerto)).start()
        puerto += 1

