import time
import sys
import json
import os

# 将搜索目录改为上一级目录
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir))
from src.scripts.util import *
from src.scripts.entity import *

def process_server(path:str):
    serverB = Server()
    with open(path, "r") as file:
        user_info = json.loads(file.read())
    serverB.set_info_from_user(user_info)
    ServerUtil.saveServerJson(serverB)

    # SyncServer生成编译相关函数
    ServerUtil.generateSyncServer(serverB)
    ServerUtil.generateSyncServerCMakeLists(serverB)
    ServerUtil.compileSyncServer(serverB)
    ServerUtil.generateExecShell(serverB.get_name())

if __name__ == "__main__":

    """
    server相关函数
    """
    # 实例化一个server
    pathA = f"{os.path.dirname(os.path.abspath(__file__))}/server_530_json/atomic_service_mbsb.json"
    pathB = f"{os.path.dirname(os.path.abspath(__file__))}/server_530_json/atomic_service_sf.json"
    pathC = f"{os.path.dirname(os.path.abspath(__file__))}/server_530_json/FusionData.json" 
    pathD = f"{os.path.dirname(os.path.abspath(__file__))}/server_530_json/ImageDetection.json"
    pathE = f"{os.path.dirname(os.path.abspath(__file__))}/server_530_json/RobotPose.json" 
    pathF = f"{os.path.dirname(os.path.abspath(__file__))}/server_530_json/atomic_service_ycl.json"
    pathG = f"{os.path.dirname(os.path.abspath(__file__))}/server_530_json/atomic_service_zlsc.json"
    process_server(pathA)
    process_server(pathB)
    process_server(pathC)
    process_server(pathD)
    process_server(pathE)
    process_server(pathF)
    process_server( pathG)