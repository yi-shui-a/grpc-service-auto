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


if __name__ == "__main__":
    Util.run_executable_in_path(
        "/root/micro_service/server_compiling/db/client/client_formal_demo_with_dds/bin/",
        "client_formal_demo_with_dds_sync_client",
    )
