from flask import Flask, request, jsonify
import socket
import threading
import json


# UDP 服务器处理函数
def receive():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("192.168.0.129", 6666))

    while True:
        data, addr = sock.recvfrom(1024)
        print(f'Received message: {data} from {addr}')

        try:
            # 尝试解析 JSON 数据
            json_data = json.loads(data.decode('utf-8'))
            print(f'Received JSON data: {json_data}')

            # 在这里处理接收到的 JSON 数据
            # 可以将数据存储在全局变量或队列中供 Flask 应用访问

        except json.JSONDecodeError:
            print('Received non-JSON data')


# 启动 UDP 服务器线程
# udp_thread = threading.Thread(target=receive)
# udp_thread.daemon = True
# udp_thread.start()
receive()