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


def test_dds():
    """
    DDS相关函数
    """
    GrpcDDSUtil.loadIdl(
        f"{os.path.dirname(os.path.abspath(__file__))}/../example/idl/example.idl"
    )
    GrpcDDSUtil.generateIdlCMakeLists("example")
    GrpcDDSUtil.compileIdl("example")

    GrpcDDSUtil.loadDDS(
        f"{os.path.dirname(os.path.abspath(__file__))}/../example/communication/dds_publisher_formal_demo.cpp"
    )
    GrpcDDSUtil.generateDDSCMakeLists("dds_publisher_formal_demo", ["example"])
    GrpcDDSUtil.compileDDS("dds_publisher_formal_demo")


if __name__ == "__main__":
    test_dds()
