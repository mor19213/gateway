import socket
import threading
import time
import requests

RCV_IP = "0.0.0.0"
RCV_PORT = 5005
TEST_IP = "192.168.0.122"
TEST_PORT = 5005
SEND_PORT = 5005
actuadores = []
username = "mor19213"
url = f"http://127.0.0.1:8000/{username}"
resp = requests.get(f"{url}/login")

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((RCV_IP, RCV_PORT))
print("UDP server up and listening")

def recieve_message():
    while True:
        try:
            data, addr = sock.recvfrom(1024)
            msg = data.decode("utf-8")
            valor = (msg.split("/")[2])
            name = (msg.split("/")[1])
            tipo = (msg.split("/")[0])
            data = {"valor": str(valor)}
            if tipo == "sensor":
                print("tipo: "+tipo)
                print("nombre: "+name)
                print("valor: "+valor+"\n")
                my_request = requests.put(f"{url}/sensores/{name}", json=data)
                #if my_request.status_code == 200:
                #    print("actualizado")
            elif tipo == "actuador":
                # add actuador to list if not already in it
                if valor == "desconectar":
                    actuador = next((actuador for actuador in actuadores if actuador["nombre"] == name), None)
                    print("actuador a eliminar: "+actuador["nombre"])
                    actuadores.remove(actuador)
                else:
                    if not any((actuador["nombre"] == name and actuador["ip"] == addr[0]) for actuador in actuadores):
                        actuadores.append({"nombre": name, "ip": addr[0], "time": time.time()})
                    else:
                        actuador = next((actuador for actuador in actuadores if actuador["nombre"] == name and actuador["ip"] == addr[0]), None)
                        actuador["time"] = time.time()
                #print(actuadores)
            elif tipo == "valActuador":
                print("tipo: Actualizar actuador")
                print("nombre: "+name)
                print("valor: "+valor+"\n")
                continue
                print(msg)
            else:
                continue
                print(data)
            

        except:
            print("Error al recibir")
            continue
    sock.close()


recieve_thread = threading.Thread(target=recieve_message)
recieve_thread.start()

send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def send_message():
    while True:
        # wait 4 seconds
        time.sleep(1)
        for actuador in actuadores:
            if actuador["time"] < time.time() - 100:
                actuadores.remove(actuador)
                print("Actuador eliminado")
                continue
            try:
                my_request = requests.get(f"{url}/actuadores/{actuador['nombre']}")
                #my_request = Request.get(actuador["nombre"])
                if my_request.status_code == 200:
                    #print("actualizado")
                    data = my_request.json()
                    data = str({'valor': str(data["valor"])})
                    dataTopic = "valActuador/"+actuador["nombre"]+"/"+data
                    send_socket.sendto(dataTopic.encode("utf-8"), (TEST_IP, TEST_PORT))
                    send_socket.sendto(data.encode("utf-8"), (actuador["ip"], SEND_PORT))
                else:
                    # remove actuador from list
                    actuadores.remove(actuador)
                    print("Actuador eliminado")

            except:
                print("Error al enviar")
                continue
    send_socket.close()

send_thread = threading.Thread(target=send_message)
send_thread.start()

test_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
def send_test():
    while True:
        try: 
            message = input("")
            test_socket.sendto(message.encode("utf-8"), (TEST_IP, TEST_PORT))
        except:
            #print("error test")
            continue
    test_socket.close()

send_test_thread = threading.Thread(target=send_test)
send_test_thread.start()