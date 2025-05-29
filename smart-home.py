import time
import random
import json
import os
import paho.mqtt.client as mqtt
from paho.mqtt.client import CallbackAPIVersion
from dotenv import load_dotenv

# ----------------------------
# Configuration and Constants
# ----------------------------

load_dotenv()  # Load environment variables from .env file

BROKER_IP = os.getenv("BROKER_IP", "localhost")
BROKER_PORT = int(os.getenv("BROKER_PORT", 1883))
DEVICE_ID = os.getenv("DEVICE_ID", "device" + str(random.randint(1, 1000)))

MQTT_TOPIC_PUBLISH = "home_status"
MQTT_TOPIC_SUBSCRIBE = "gpio/heat"

# ----------------------------
# MQTT Callbacks
# ----------------------------

def on_message(client, userdata, msg):
    """Handles incoming MQTT messages (e.g., commands)."""
    topic = msg.topic
    try:
        command_data = json.loads(msg.payload.decode())
    except json.JSONDecodeError:
        print("Invalid command format")
        return

    if topic == MQTT_TOPIC_SUBSCRIBE:
        handle_gpio_command(client, command_data)

def handle_gpio_command(client, command_data):
    """Handles 'gpio/heat' commands and sends back an acknowledgment."""
    state = command_data.get("state", "UNKNOWN")
    desired_temp = command_data.get("desiredtemp", None)

    if state == "HEAT_ON":
        print("[GPIO] Heating ON (simulated HIGH)")
    elif state == "COOL_ON":
        print("[GPIO] Cooling ON (simulated LOW)")
    else:
        print("[GPIO] Unknown state")

    ack_payload = {
        "device_id": DEVICE_ID,
        "type": "ack",
        "value": f"{state} for {desired_temp}°C"
    }
    client.publish(MQTT_TOPIC_PUBLISH, json.dumps(ack_payload))

# ----------------------------
# Sensor Data Generation
# ----------------------------

def generate_temperature(prev_temp):
    """Simulates temperature fluctuation."""
    return round(random.uniform(prev_temp - 1, prev_temp + 1), 1)

def generate_humidity(prev_hum):
    """Simulates humidity fluctuation."""
    return round(random.uniform(prev_hum - 2, prev_hum + 2), 0)

def publish_sensor_data(client, temperature, humidity):
    """Publishes temperature and humidity data to the MQTT broker."""
    temp_payload = {
        "device_id": DEVICE_ID,
        "type": "temperature",
        "value": temperature,
        "unit": "°C"
    }

    hum_payload = {
        "device_id": DEVICE_ID,
        "type": "humidity",
        "value": humidity,
        "unit": "%"
    }

    client.publish(MQTT_TOPIC_PUBLISH, json.dumps(temp_payload))
    client.publish(MQTT_TOPIC_PUBLISH, json.dumps(hum_payload))
    print("Sent:", temp_payload, hum_payload)

# ----------------------------
# Main Execution
# ----------------------------

def main():
    client = mqtt.Client(callback_api_version=CallbackAPIVersion.VERSION2)
    client.on_message = on_message
    while True:
        try:
            client.connect(BROKER_IP, BROKER_PORT, 60)
            break
        except Exception as e:
            print(f"Waiting for MQTT broker: {e}")

    client.subscribe(MQTT_TOPIC_SUBSCRIBE)
    client.loop_start()

    temperature = round(random.uniform(15.0, 30.0), 0)
    humidity = round(random.uniform(20.0, 60.0), 1)

    while True:
        publish_sensor_data(client, temperature, humidity)
        temperature = generate_temperature(temperature)
        humidity = generate_humidity(humidity)
        time.sleep(5)

if __name__ == "__main__":
    main()
