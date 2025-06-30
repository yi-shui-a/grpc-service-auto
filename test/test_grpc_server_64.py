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
    pathA = f"{os.path.dirname(os.path.abspath(__file__))}/server_64_json/atomic_show_cgsj.json"
    pathB = f"{os.path.dirname(os.path.abspath(__file__))}/server_64_json/atomic_show_ddpc.json"
    pathC = f"{os.path.dirname(os.path.abspath(__file__))}/server_64_json/atomic_show_ddzt.json" 
    pathD = f"{os.path.dirname(os.path.abspath(__file__))}/server_64_json/atomic_show_hjrd.json"
    pathE = f"{os.path.dirname(os.path.abspath(__file__))}/server_64_json/atomic_show_sjrh.json" 
    pathF = f"{os.path.dirname(os.path.abspath(__file__))}/server_64_json/atomic_show_ycl.json"
    pathG = f"{os.path.dirname(os.path.abspath(__file__))}/server_64_json/atomic_show_ysdd.json"
    pathH = f"{os.path.dirname(os.path.abspath(__file__))}/server_64_json/atomic_show_zlsc.json"
    pathI = f"{os.path.dirname(os.path.abspath(__file__))}/server_64_json/atomic_show_ztjs.json" 
    pathJ = f"{os.path.dirname(os.path.abspath(__file__))}/server_64_json/atomic_show_zxzl.json"
    pathK = f"{os.path.dirname(os.path.abspath(__file__))}/server_64_json/atomic_show_ALL.json"
    process_server(pathA)
    process_server(pathB)
    process_server(pathC)
    process_server(pathD)
    process_server(pathE)
    process_server(pathF)
    process_server(pathG)
    process_server(pathH)
    process_server(pathI)
    process_server(pathJ)
    process_server(pathK)