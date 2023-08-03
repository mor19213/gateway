# Gateway 
## Instalaciones

### Python
```bash
sudo apt install python3-pip
```

### MQTT
```bash
sudo apt install -y mosquitto
```

### AMQP
https://www.rabbitmq.com/install-debian.html#manual-installation
```bash
## Install Erlang packages
sudo apt-get install -y erlang-base \
                        erlang-asn1 erlang-crypto erlang-eldap erlang-ftp erlang-inets \
                        erlang-mnesia erlang-os-mon erlang-parsetools erlang-public-key \
                        erlang-runtime-tools erlang-snmp erlang-ssl \
                        erlang-syntax-tools erlang-tftp erlang-tools erlang-xmerl

## Install rabbitmq-server and its dependencies
sudo apt-get install rabbitmq-server -y --fix-missing
```

#### Dependencias de python
```bash
pip install paho-mqtt
```


### Docker


## Configuracion

## Pruebas
### pruebas mosquitto
```bash
sudo apt install mosquitto-clients
```
