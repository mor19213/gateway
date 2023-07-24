# program to recieve and send udp messages
import socket
import threading

import sys
sys.path.append("..")
from my_requests import plataformaRequest

RCV_IP = "0.0.0.0"
RCV_PORT = 5005
SEND_IP = "192.168.0.122"
SEND_PORT = 5005
Request = plataformaRequest("mor19213")

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
            print("tipo: "+tipo)
            print("nombre: "+name)
            print("valor: "+valor)
            data = {"valor": valor}
            if tipo == "sensor":
                my_request = Request.put(name, data)
            elif tipo == "actuador":
                my_request = Request.get(name)
            else:
                continue
            if my_request.status_code == 200:
                print("actualizado")
                data = my_request.json()
                data = str({'valor': str(data["valor"])})
                print(data)
            else:
                print(my_request)

        except KeyboardInterrupt:
            print("Keyboard Interrupt recieve")
            break
    sock.close()

recieve_thread = threading.Thread(target=recieve_message)
recieve_thread.start()

send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def send_message():
    while True:
        try:
            message = input("")
            send_socket.sendto(message.encode("utf-8"), (SEND_IP, SEND_PORT))
        except KeyboardInterrupt:
            print("Keyboard Interrupt send")
            break
    send_socket.close()

send_message()
recieve_thread.join()