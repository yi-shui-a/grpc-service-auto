import time
import sys
import json
import os

# 将搜索目录改为上一级目录
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir))

from src.scripts.util.AtomServiceUtil import AtomServiceUtil
from src.scripts.util.GrpcMethodUtil import GrpcMethodUtil
from src.scripts.util.ServerUtil import ServerUtil
from scripts.entity.Server import Server
from src.scripts.util.Util import Util
from src.scripts.util.DDSUtil import DDSUtil


def test_server():
    # 实例化一个server
    serverB = Server()
    with open(
        f"{os.path.dirname(os.path.abspath(__file__))}/user_info.json", "r"
    ) as file:
        user_info = json.loads(file.read())
    serverB.set_info_from_user(user_info)
    serverB.saveServerJson()

    # SyncServer生成编译相关函数
    ServerUtil.generateSyncServer(serverB)
    ServerUtil.generateSyncServerCMakeLists(serverB)
    ServerUtil.compileSyncServer(serverB)


if __name__ == "__main__":
    test_server()
