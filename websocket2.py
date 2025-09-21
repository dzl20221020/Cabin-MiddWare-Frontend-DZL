
# -*- coding: utf-8 -*-

import paho.mqtt.client as mqtt
import os

# EMQX配置
broker = '127.0.0.1'  # EMQX代理地址
port = 1883  # 代理端口
topic = '/test'  # 订阅的主题
output_file = 'mqtt_messages.txt'  # 存储接收到消息的文件
username = 'admin'  # 用户名
password = 'admin'  # 密码

# 回调函数，当连接成功时调用
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to EMQX Broker!")
        client.subscribe(topic)  # 连接成功后订阅主题
    else:
        print(f"Failed to connect, return code {rc}")

# 回调函数，当接收到消息时调用
def on_message(client, userdata, msg):
    message = msg.payload.decode('utf-8')
    print(f"Received message: {message}")
    # 将消息存储到文件中
    with open(output_file, 'a') as f:
        f.write(message + '\n')

# 创建MQTT客户端对象
client = mqtt.Client()

# 设置用户名和密码
client.username_pw_set(username, password)

# 绑定回调函数
client.on_connect = on_connect
client.on_message = on_message

# 连接到EMQX代理
client.connect(broker, port, 60)

# 开始订阅
client.loop_forever()