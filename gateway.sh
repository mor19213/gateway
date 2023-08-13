#!/bin/bash

kill $(lsof -t -i :5005)

# Set the PYTHONPATH
export PYTHONPATH=$PYTHONPATH:..

# Launch Python scripts in the background
python3.9 bluetooth/bt_messages.py &
python3 udp/udp_messages.py &
python3 mqtt/mqtt_messages.py &
