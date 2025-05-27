import paho.mqtt.client as mqtt
import time
import random
import json

broker_ip = "192.168.1.9"
client = mqtt.Client()

def on_message(client, userdata, msg):
    command = msg.payload.decode()
    topic = msg.topic

    if topic == "gpio/heat":
        if command == "HEAT_ON":
            print("[GPIO] Heating ON (simulated HIGH)")
        elif command == "COOL_ON":
            print("[GPIO] Cooling ON (simulated LOW)")

client.on_message = on_message
client.connect(broker_ip, 1883, 60)
client.subscribe("gpio/heat")

client.loop_start()  # Start background thread to listen for messages


device_id = "device"+str(random.randint(1, 1000))
temperature = round(random.uniform(15.0, 30.0), 0)
humidity = round(random.uniform(20.0, 60.0), 1)
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
    humidity = round(random.uniform(humidity-2, humidity+2), 0)
    temperature = round(random.uniform(temperature-1, temperature+1), 1)

    client.publish("my_status", json.dumps(temp_payload))
    client.publish("my_status", json.dumps(hum_payload))

    print("Sent:", temp_payload, hum_payload)
    time.sleep(5)
