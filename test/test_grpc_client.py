import time
import sys
import json
import os

# 将搜索目录改为上一级目录
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir))

from src.scripts.util.Util import Util
from src.scripts.util.GrpcDDSUtil import GrpcDDSUtil
from scripts.entity.Client import Client
from src.scripts.util.ClientUtil import ClientUtil


def test_client():
    """
    假装构造一个client
    """
    # 构造client
    client = Client()
    client.set_name("client_formal_demo_with_dds")
    client.add_dds_module("example")
    client.add_service("atomic_service_mbsb")
    client.add_service("atomic_service_sf")

    ClientUtil.generateSyncClientCMakeLists(client)
    ClientUtil.compileSyncClient(client)


if __name__ == "__main__":
    test_client()
