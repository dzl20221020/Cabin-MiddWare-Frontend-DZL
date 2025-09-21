# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2024/4/17 14:51
# @Author : DZL
# @File : gazepointservice.py
# @Software: PyCharm
import requests

import global_vars


class MusicService(object):
    def __init__(self):
        pass
    # 播放音乐函数
    def playMusic(self):
        # 定义接口的 URL
        url = global_vars.SERVER_ADDRESS + "music/play"

        # 定义要发送的数据（如果有的话）
        payload = {
            # 这里添加你需要发送的数据，如果有的话
        }

        # 发送 POST 请求
        try:
            response = requests.get(url, json=payload)
        except Exception as e:
            print(repr(e))

        # 检查响应状态码
        if response.status_code == 200:
            print("Play successful")
        else:
            print("Play failed")

        # 播放音乐函数

    def stopMusic(self):
        # 定义接口的 URL
        url = "http://localhost:8888/music/stop"

        # 定义要发送的数据（如果有的话）
        payload = {
            # 这里添加你需要发送的数据，如果有的话
        }

        # 发送 POST 请求
        try:
            response = requests.get(url, json=payload)
        except Exception as e:
            print(repr(e))

        # 检查响应状态码
        if response.status_code == 200:
            print("Stop successful")
        else:
            print("Stop failed")