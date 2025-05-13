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


if __name__ == "__main__":
    # 构造client
    client = Client()
    client.set_name("client_formal_demo_with_dds")
    client.add_dds_topic("example")
    client.add_service("atomic_service_mbsb")
    client.add_service("atomic_service_sf")

    # 生成编译client的cmakeList
    ClientUtil.generateSyncClientCMakeLists(client)
    # 编译client
    ClientUtil.compileSyncClient(client)
