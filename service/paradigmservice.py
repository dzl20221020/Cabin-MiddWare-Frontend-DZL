# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2024/4/17 14:51
# @Author : DZL
# @File : gazepointservice.py
# @Software: PyCharm
import requests

import global_vars


class ParadigmService(object):
    def __init__(self):
        self.calibraeFlag = False   # 是否校准的标志

        # 获取所有范式信息

    def startParadigm(self):
        # 定义接口的 URL
        url = global_vars.SERVER_ADDRESS + "paradigm/executeParadigm/" + global_vars.experiment_id

        # 定义要发送的数据（如果有的话）
        payload = {
            # 这里添加你需要发送的数据，如果有的话
        }

        # 发送 GET 请求
        try:
            response = requests.get(url, json=payload)
            data = response.json()  # 解析 JSON 响应数据
            return data
        except Exception as e:
            print(repr(e))

        # 检查响应状态码
        if response.status_code == 200:
            print("start successful")
        else:
            print("start failed")

    # 获取所有范式信息
    def getAllParadigm(self):
        # 定义接口的 URL
        url = global_vars.SERVER_ADDRESS + "paradigm/getAllParadigm"

        # 定义要发送的数据（如果有的话）
        payload = {
            # 这里添加你需要发送的数据，如果有的话
        }

        # 发送 GET 请求
        try:
            response = requests.get(url, json=payload)
            data = response.json()  # 解析 JSON 响应数据
            return data
        except Exception as e:
            print(repr(e))

        # 检查响应状态码
        if response.status_code == 200:
            print("paradigm successful")
        else:
            print("paradigm failed")


    # 根据id获取范式信息
    def getParadigmById(self,id):
        # 定义接口的 URL
        url = "http://localhost:8888/paradigm/getParadigmById/"+id

        # 定义要发送的数据（如果有的话）
        payload = {
            # 这里添加你需要发送的数据，如果有的话
        }

        # 发送 GET 请求
        try:
            response = requests.get(url, json=payload)
            data = response.json()  # 解析 JSON 响应数据
            return data
        except Exception as e:
            print(repr(e))

        # 检查响应状态码
        if response.status_code == 200:
            print("paradigm successful")
        else:
            print("paradigm failed")


    # 根据id获取范式信息
    def selectParadigmById(self):
        # 定义接口的 URL
        url = "http://localhost:8888/paradigm/selectParadigmById/"+ global_vars.paradigm_id

        # 定义要发送的数据（如果有的话）
        payload = {
            # 这里添加你需要发送的数据，如果有的话
        }

        # 发送 GET 请求
        try:
            response = requests.get(url, json=payload)
            data = response.json()  # 解析 JSON 响应数据
            return data
        except Exception as e:
            print(repr(e))

        # 检查响应状态码
        if response.status_code == 200:
            print("select successful")
        else:
            print("select failed")
