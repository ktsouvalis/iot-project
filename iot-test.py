import paho.mqtt.client as mqtt
import time
import random
import json

client = mqtt.Client()
client.connect("192.168.1.9", 1883, 60)

device_id = "device-001"
temperature = round(random.uniform(10.0, 30.0), 2)
humidity = round(random.uniform(20.0, 60.0), 2)
while True:
    

    temp_payload = {
        "device_id": device_id,
        "type": "temperature",
        "value": temperature,
    }

    hum_payload = {
        "device_id": device_id,
        "type": "humidity",
        "value": humidity,
    }
    humidity = round(random.uniform(humidity-2, humidity+2), 2)
    temperature = round(random.uniform(temperature-1, temperature+1), 2)

    client.publish("my_status", json.dumps(temp_payload))
    client.publish("my_status", json.dumps(hum_payload))

    print("Sent:", temp_payload, hum_payload)
    time.sleep(5)
