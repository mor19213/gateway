from my_requests import plataformaRequest
import bluetooth
import threading

Request = plataformaRequest("mor19213")

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
                #print("Recibido: "+recibido)
                if recibido.find("sensor") != -1:
                    nombre = recibido.split("/")[1]
                    valor = recibido.split("/")[2]
                    valor = valor.split("\n")[0]
                    try:
                        valor = float(valor)
                        data = {"valor": valor}
                    except:
                        continue
                    print(nombre +": "+str(data))
                    my_request = Request.put(nombre, data)
                elif recibido.find("actuador") != -1:
                    #print("Recibido: "+recibido)
                    nombre = recibido.split("/")[1]
                    nombre = nombre.split("\n")[0]
                    if nombre == "actuador":
                        continue
                    my_request = Request.get(nombre)
                    if my_request.status_code == 200:
                        #print("actualizado")
                        data = my_request.json()
                        data = str({'valor': str(data["valor"])})
                        print(nombre +": "+str(data))
                        sock.send("{}".format(data))
                    else:
                        print("Error en request")
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
        #device(name, sock, puerto)
        threading.Thread(target=device, args=(name, sock, puerto)).start()
        puerto += 1

