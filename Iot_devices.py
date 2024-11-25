import time
import paho.mqtt.client as mqtt
import random

# MQTT Settings
BROKER = "broker.hivemq.com"
PORT = 1883
TOPIC_MOTION = "home/motion"
TOPIC_TEMP_HUMID = "home/tempHumid"

# Simulating sensor data (replace with actual sensor code)
def read_motion_sensor():
    return random.choice(["Motion detected", "No motion"])

def read_temp_humidity():
    temp = random.uniform(20, 30)
    humid = random.uniform(40, 60)
    return f"Temperature: {temp:.2f}°C, Humidity: {humid:.2f}%"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print(f"Failed to connect, return code {rc}")

client = mqtt.Client()
client.on_connect = on_connect
client.connect(BROKER, PORT, 60)
client.loop_start()

try:
    while True:
        # Publish motion sensor data
        motion = read_motion_sensor()
        client.publish(TOPIC_MOTION, motion)
        print(f"Published: {motion}")

        # Publish temperature and humidity
        temp_humid = read_temp_humidity()
        client.publish(TOPIC_TEMP_HUMID, temp_humid)
        print(f"Published: {temp_humid}")

        time.sleep(2)
except KeyboardInterrupt:
    print("Stopping...")
    client.loop_stop()
