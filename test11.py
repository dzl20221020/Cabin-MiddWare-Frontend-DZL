import paho.mqtt.client as mqtt
import json
import random
import time

# MQTT broker details
broker = "111.231.12.252"  # 替换为你的MQTT代理地址
port = 1883  # MQTT代理端口，通常为1883
topic = "/test"  # 替换为你要发布到的主题
username = "admin"  # 替换为你的MQTT用户名
password = "admin"  # 替换为你的MQTT密码

# Create a new MQTT client instance
client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected successfully")
    else:
        print(f"Connect failed with code {rc}")

# Set username and password
client.username_pw_set(username, password)

# Connect to the MQTT broker
client.on_connect = on_connect
client.connect(broker, port, 60)

def generate_random_data():
    return [random.randint(1, 100) for _ in range(8)]

def create_message():
    message = {
        "header": {
            "device_id": "unique_device_identifier",
            "protocol_version": "v1.0",
            "sampling_rate": 60,
            "channels": 8,
            "type": "hr"
        },
        "data": generate_random_data()
    }
    return message

try:
    client.loop_start()
    while True:
        msg = create_message()
        msg_json = json.dumps(msg)
        client.publish(topic, msg_json)
        print(f"Message sent: {msg_json}")
        time.sleep(0.004)  # 每秒发送一次消息
except KeyboardInterrupt:
    print("Exiting...")
finally:
    client.loop_stop()
    client.disconnect()
