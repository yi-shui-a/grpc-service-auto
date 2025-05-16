from flask import Flask, send_from_directory
from flask_socketio import SocketIO
from flask import Flask, request, jsonify
from gevent import pywsgi
import threading
from geventwebsocket.handler import WebSocketHandler
import json
import socket
import time
import datetime
import multiprocessing
import random
import paramiko
from scp import SCPClient

import sys
import os

imginfo = {}
filename = f"{os.path.dirname(os.path.abspath(__file__))}/nameinfo_new.txt"
node2 = {"ip": "192.168.0.106", "port": 6666}
node1 = {"ip": "192.168.0.105", "port": 6666}
node3 = {"ip": "192.168.0.190", "port": 22}
node3_user = "su"
node3_password = "root"
# 本地ip和端口
node4 = {"ip": "192.168.0.129", "port": 8022}
node5 = {"ip": "192.168.0.129", "port": 8023}

# 创建 Flask 应用实例
app = Flask(__name__, static_folder="dist", template_folder="templates")
# 设置 Flask 的加密密钥，用于会话（session）安全。在生产环境中应使用​​随机生成的强密钥​​，而不是硬编码。
app.config["SECRET_KEY"] = "secret!"
# 初始化 flask-socketio，用于 WebSocket 通信。
# cors_allowed_origins="*" 允许​​所有来源（跨域请求）​​，适用于开发环境，但生产环境应限制为可信域名。

socketio = SocketIO(app, cors_allowed_origins="*")

# 初始化共享数据和锁
# 创建一个​​共享内存数组​​，可以在多个进程之间共享数据。
# "d" 表示 double（双精度浮点数），"i" 表示 int（整数）。
cpuUsage = multiprocessing.Array("d", [0.0, 0.0, 0.0, 0.0])  # 'd' 表示双精度浮点数
# 提供​​进程锁​​，防止多个进程同时修改共享数据（避免竞争条件）。
# 修改数据前必须 acquire()，修改后 release()：
cpu_lock = multiprocessing.Lock()
# hisCpuUsage = [0.0, 0.0, 0.0, 0.0]
memoryUsage = multiprocessing.Array("d", [0.0, 0.0, 0.0, 0.0])
memory_lock = multiprocessing.Lock()
# hisMemoryUsage = [0.0, 0.0, 0.0, 0.0]
runningContainer = multiprocessing.Array("i", [0, 0, 0, 0])
running_lock = multiprocessing.Lock()
# hisRunningContainer = [0, 0, 0, 0]
diskUsage = multiprocessing.Array("d", [0.0, 0.0, 0.0, 0.0])
disk_lock = multiprocessing.Lock()


# 队列用于​​进程间通信​​（IPC），允许不同进程发送和接收消息。
queue = multiprocessing.Queue()


def background_thread():

    while not thread_stop_event.is_set():
        time.sleep(10)
        socketio.emit("message", {"type": "cpu", "data": cpuUsage[:]})
        socketio.emit("message", {"type": "disk", "data": diskUsage[:]})
        socketio.emit("message", {"type": "memory", "data": memoryUsage[:]})
        socketio.emit("message", {"type": "running", "data": runningContainer[:]})

        # if (cpuUsage[:] != hisCpuUsage[:]):
        #     print("cpu" + str(cpuUsage[:]))
        #     print("disk" + str(diskUsage[:]))
        #     socketio.emit('message', {'type': 'cpu', 'data': cpuUsage[:]})
        #     socketio.emit('message', {'type': 'disk', 'data': diskUsage[:]})
        #     # 使用切片操作进行复制赋值
        #     hisCpuUsage[:] = cpuUsage[:]
        #
        # if (memoryUsage[:] != hisMemoryUsage[:]):
        #     print("memory" + str(memoryUsage[:]))
        #     socketio.emit('message', {'type': 'memory', 'data': memoryUsage[:]})
        #     # 使用切片操作进行复制赋值
        #     hisMemoryUsage[:] = memoryUsage[:]
        #
        # if (runningContainer[:] != hisRunningContainer[:]):
        #     print("running" + str(runningContainer[:]))
        #     socketio.emit('message', {'type': 'running', 'data': runningContainer[:]})
        #     # 使用切片操作进行复制赋值
        #     hisRunningContainer[:] = runningContainer[:]


# 读取服务名-镜像映射表
# 从指定文件中读取服务名 - 镜像名的映射关系，并将这些映射关系存储在全局变量 imginfo 字典（全局变量）中。
def readImgInfo():
    imginfo.clear()
    with open(filename, "r", encoding="utf-8") as file:
        line = file.readline()
        counts = 1
        while line:
            if counts >= 50000000:
                break
            line = file.readline()
            data = "".join(line).strip("\n")
            if len(data) > 2:
                info = data.split("-")
                imginfo[info[0]] = info[1]
            counts += 1


# 向节点发送json数据
def sendJson(node, data):
    """
    通过 UDP 向指定节点发送 JSON 数据。
    :param node: 节点信息，包含 IP 和端口
    :param data: 要发送的数据
    """
    udp_addr = (node["ip"], node["port"])
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.sendto(str(data).encode("utf-8"), udp_addr)


# json数据转化 将服务名替换为对应的镜像名
def jsonTran(data):
    # print(data)
    for i in data:
        for j in i["children"]:
            temp = j["text"]
            j["text"] = imginfo[temp]
    return data


@app.route("/")
def index():
    """
    根路由，返回静态文件夹中的 index.html 文件。
    """
    return send_from_directory(app.static_folder, "index.html")


@app.route("/echo")
def echo_socket(ws):
    """
    WebSocket 路由，接收客户端消息并返回当前时间。
    """
    print("connection start")
    while not ws.closed:
        msg = ws.receive()  # 同步阻塞
        print(msg)
        now = datetime.datetime.now().isoformat()
        ws.send(now)  # 发送数据
        time.sleep(1)


def create_ssh_client(node, user, password):
    """
    创建 SSH 客户端并连接到指定节点。
    :param node: 节点信息
    :param user: 用户名
    :param password: 密码
    :return: SSH 客户端实例
    """
    # 创建 SSH 客户端实例
    client = paramiko.SSHClient()
    # 自动添加策略，保存服务器的主机名和密钥信息
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # 连接到服务器
    client.connect(node["ip"], node["port"], user, password)
    return client


@app.route("/deploy-meta", methods=["POST"])
def receive_json_data():
    """
    处理前端发送的 JSON 数据，进行数据转换和发送，同时更新 JSON 文件并通过 SSH 传输。
    """
    # 获取前端发送的JSON数据
    data = request.get_json()

    # 检查是否成功获取到数据
    if not data:
        return jsonify({"error": "No JSON data received"}), 400

    # 获取数据
    processed_data = {"message": f"Received: {data}"}
    tempData = processed_data["message"].strip("Received: ").replace("'", '"')
    # str数据转json 更换名字
    json_obj = json.loads(tempData)
    deployData = jsonTran(json_obj)
    # json转str
    senddata = str(deployData).replace("'", '"')
    print(senddata)
    sendJson(node1, senddata)
    sendJson(node2, senddata)

    with open("node3_data.json", "w", encoding="utf-8") as json_file:
        json_file.write(senddata)

    try:
        # 创建 SSH 客户端
        ssh_client = create_ssh_client(node3, node3_user, node3_password)

        # 创建 SCP 客户端
        scp = SCPClient(ssh_client.get_transport())
        # 发送文件
        scp.put(
            "D:\\chongqing\\deployfile\\deployfile\\sdw\\run\\sdwqz\\node3_data.json",
            "/home/su/works/630/json/",
        )
        print(
            f"File node3_data.json successfully sent to {node3['ip']}:su/works/630/json/"
        )
    except Exception as e:
        print(f"Error sending file: {e}")
    finally:
        # 关闭 SCP 和 SSH 客户端
        scp.close()
        ssh_client.close()

    # 返回响应，这里使用JSON格式返回
    return jsonify(processed_data), 200


@app.route("/<path:path>")
def static_proxy(path):
    return send_from_directory(app.static_folder, path)


def receive_data(
    node,
    cpu_list,
    memory_list,
    running_list,
    disk_list,
    cpu_lock,
    memory_lock,
    running_lock,
    disk_lock,
):
    """
    通过 UDP 接收数据，根据系统版本更新 CPU、内存、磁盘和运行容器信息。
    :param node: 节点信息
    :param cpu_list: CPU 使用情况列表
    :param memory_list: 内存使用情况列表
    :param running_list: 运行容器数量列表
    :param disk_list: 磁盘使用情况列表
    :param cpu_lock: CPU 锁
    :param memory_lock: 内存锁
    :param running_lock: 运行容器锁
    :param disk_lock: 磁盘锁
    """
    print("receive ready")
    # 创建套接字
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    address = (node["ip"], node["port"])
    sock.bind(address)

    print("Waiting for data...")

    while True:
        header, _ = sock.recvfrom(4096)  #
        data, _ = sock.recvfrom(65535)  #
        # print("header:{} ".format(header))
        # print("data:{}".format(data))

        header_Info = json.loads(header.decode("utf-8"))
        Data_Info = json.loads(data.decode("utf-8"))
        header_type = header_Info["type"]
        # if header_type == 1:
        #     print("system_version: {}".format(Data_Info['system_version']))
        #     print("kernel_version: {}".format(Data_Info['kernel_version']))
        #     print("cpu_usage: {}".format(Data_Info['cpu_usage']))
        #     print("memory_usage: {}".format(Data_Info['memory_usage']))
        # if header_type == 2:
        #     print("cardNum: {}".format(Data_Info['cardNum']))
        #     print("total_containers: {}".format(Data_Info['total_containers']))
        #     print("image_count: {}".format(Data_Info['image_count']))
        #     print("running_containers: {}".format(Data_Info['running_containers']))
        #     print("docker_version: {}".format(Data_Info['docker_version']))
        #     for i in range(15):
        #         print("container_info.container_id{}: {}".format(i, Data_Info['container_info'][i]['container_id']))
        #         print("ContainerInspect.container_id{}: {}".format(i, Data_Info['container_info'][i]['ContainerInspect']['container_id']))
        #         print("container_info.container_created{}: {}".format(i, Data_Info['container_info'][i]['ContainerInspect']['container_created']))
        #         print("container_info.container_path{}: {}".format(i, Data_Info['container_info'][i]['ContainerInspect']['container_path']))
        #         print("container_info.container_args{}: {}".format(i, Data_Info['container_info'][i]['ContainerInspect']['container_args']))
        #         print("container_info.status{}: {}".format(i, Data_Info['container_info'][i]['ContainerInspect']['container_status']['status']))
        #         print("container_info.running{}: {}".format(i, Data_Info['container_info'][i]['ContainerInspect']['container_status']['running']))
        #         print("container_info.paused{}: {}".format(i, Data_Info['container_info'][i]['ContainerInspect']['container_status']['paused']))
        #         print("container_info.restarting{}: {}".format(i, Data_Info['container_info'][i]['ContainerInspect']['container_status']['restarting']))
        #         print("container_info.oomkilled{}: {}".format(i, Data_Info['container_info'][i]['ContainerInspect']['container_status']['oomkilled']))
        #         print("container_info.dead{}: {}".format(i, Data_Info['container_info'][i]['ContainerInspect']['container_status']['dead']))
        #         print("container_info.pid{}: {}".format(i, Data_Info['container_info'][i]['ContainerInspect']['container_status']['pid']))
        #         print("\n")
        # print("================================== \n")

        try:
            cpu_lock.acquire()
            disk_lock.acquire()
            if "system_version" in Data_Info and "cpu_usage" in Data_Info:
                if Data_Info["system_version"] == "Ubuntu 20.04.6 LTS":
                    cpu_list[0] = float("{:.2f}".format(float(Data_Info["cpu_usage"])))
                    disk_list[0] = float("{:.2f}".format(random.uniform(30, 31)))
                elif Data_Info["system_version"] == "22.03 LTS dracut-055-4.oe2203":
                    cpu_list[1] = float("{:.2f}".format(float(Data_Info["cpu_usage"])))
                    disk_list[1] = float("{:.2f}".format(random.uniform(30, 31)))
        except Exception as err:
            raise err
        finally:
            cpu_lock.release()
            disk_lock.release()

        try:
            memory_lock.acquire()
            if "system_version" in Data_Info and "memory_usage" in Data_Info:
                if Data_Info["system_version"] == "Ubuntu 20.04.6 LTS":
                    memory_list[0] = float(
                        "{:.2f}".format(
                            float(Data_Info["memory_usage"]) / (1024 * 1024 * 1024)
                        )
                    )
                elif Data_Info["system_version"] == "22.03 LTS dracut-055-4.oe2203":
                    memory_list[1] = float(
                        "{:.2f}".format(
                            Data_Info["memory_usage"] / (1024 * 1024 * 1024)
                        )
                    )
        except Exception as err:
            raise err
        finally:
            memory_lock.release()

        try:
            running_lock.acquire()
            if "cardNum" in Data_Info and "running_containers" in Data_Info:
                running_list[int(Data_Info["cardNum"]) - 1] = int(
                    Data_Info["running_containers"]
                )
        except Exception as err:
            raise err
        finally:
            running_lock.release()


@socketio.on("connect")
def handle_connect():
    print("Client connected")
    socketio.emit("message", {"data": "connected"})


@socketio.on("disconnect")
def handle_disconnect():
    print("Client connected")
    socketio.emit("message", {"data": "disconnected"})


if __name__ == "__main__":

    readImgInfo()
    # jsonTran(testJsonData)
    # app.run(debug=True)
    # 接收数据
    receive1 = multiprocessing.Process(
        target=receive_data,
        args=(
            node4,
            cpuUsage,
            memoryUsage,
            runningContainer,
            diskUsage,
            cpu_lock,
            memory_lock,
            running_lock,
            disk_lock,
        ),
    )
    receive2 = multiprocessing.Process(
        target=receive_data,
        args=(
            node5,
            cpuUsage,
            memoryUsage,
            runningContainer,
            diskUsage,
            cpu_lock,
            memory_lock,
            running_lock,
            disk_lock,
        ),
    )

    receive1.start()
    receive2.start()

    thread = threading.Thread(target=background_thread)
    thread_stop_event = threading.Event()
    thread.start()

    server = pywsgi.WSGIServer(("0.0.0.0", 5000), app, handler_class=WebSocketHandler)
    print("Server started")
    server.serve_forever()

    # 等待接收线程结束
    receive1.join()
    print("接收进程1结束")
    receive2.join()
    print("接收进程2结束")
    thread.join()
    print("发送线程结束")

    print("Main thread exiting.")
