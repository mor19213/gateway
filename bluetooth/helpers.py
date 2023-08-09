import bluetooth

def scan():
    print("Scanning for bluetooth devices:")
    devices = bluetooth.discover_devices(lookup_names = True, lookup_class = True)
    return devices

    for addr, name, device_class in devices:
        print("\n")
        print("Device:")
        print("Device Name: %s" % (name))
        print("Device MAC Address: %s" % (addr))
        print("Device Class: %s" % (device_class))
        print("\n")

dispositivos = scan()
print(dispositivos)

for addr, name, device_class in dispositivos:
    if name.find("sensor") != -1:
        print("sensor")
    if name.find("actuador") != -1:
        print("actuador")
    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    sock.connect((addr, 1))
    message = "Hello, Bluetooth!"
    sock.send("{}".format(message))
    while True:
        data = sock.recv(2048)
        if not data:
            break
        print(f"Recibido: {data.decode('utf-8')}")
    sock.close()
    break