#### As an example below shell script can be used to execute this every 300s.
####!/bin/bash
####while true
####do
####        /usr/bin/sudo python3 /path/of/the/python/script.sh
####done

#!/usr/bin/python
import sys
import time
import paho.mqtt.client as mqtt

broker_url = "<IP_Address_of_MQTT_broker>"
broker_port = <MQTT_Broker_port>

def on_connect(client, userdata, flags, rc):
        print("Connected With Result Code: {}".format(rc))

def on_message(client, userdata, message):
        print("Message Recieved: "+message.payload.decode())
        file_name=message.payload.decode()
        file_path="/home/demouser/nagios/node-check/logs/"+file_name+".ok"
        file1 = open(file_path, 'w')
        file1.write(message.payload.decode()+" is up and running\n")
        file1.close()

def on_disconnect(client, userdata, rc):
        print("Client Got Disconnected")

client = mqtt.Client("Nagios_NodeChecker")
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message
client.username_pw_set(username="<mqtt_username>",password="<mqtt_password>")

client.connect(broker_url, broker_port)
client.subscribe(topic="nagios/node_check", qos=2)
client.message_callback_add("nagios/node_check", on_message)

client.loop_start()
time.sleep(300)
client.loop_stop()

