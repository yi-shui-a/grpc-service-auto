import time
import sys
import json
import os

# 将搜索目录改为上一级目录
sys.path.append(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, os.pardir)
)

from src.scripts.util import *
from src.scripts.entity import *


"""
生成server的json文件和代码并编译
"""
if __name__ == "__main__":
    # 实例化一个server对象
    serverB = Server()
    with open(
        f"{os.path.dirname(os.path.abspath(__file__))}/../user_info.json", "r"
    ) as file:
        user_info = json.loads(file.read())
    serverB.set_info_from_user(user_info)
    # 保存server的json文件
    ServerUtil.saveServerJson(serverB)

    # 生成server的代码
    ServerUtil.generateSyncServer(serverB)
    # 生成编译server的cmake
    ServerUtil.generateSyncServerCMakeLists(serverB)
    # 编译server
    ServerUtil.compileSyncServer(serverB)
