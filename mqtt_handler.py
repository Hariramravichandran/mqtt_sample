import random
import threading
import time
from datetime import datetime
import paho.mqtt.client as mqtt

from db import get_collection

MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "test/status"

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

def on_message(client, userdata, msg):
    collection =get_collection()
    message = {
        "status": int(msg.payload),
        "timestamp": datetime.now()
    }
    collection.insert_one(message)
    

mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

def start_mqtt_client():
    mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
    mqtt_client.loop_start()
    mqtt_client.subscribe(MQTT_TOPIC)

def close_mqtt_client():
    mqtt_client.loop_stop()
    mqtt_client.disconnect()
    print("MQTT client disconnected.")

def emit_messages():
    while True:
        status = random.randint(0, 6)
        mqtt_client.publish(MQTT_TOPIC, status)
        time.sleep(1)

thread = threading.Thread(target=emit_messages)
thread.daemon = True
thread.start()

