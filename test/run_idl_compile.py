import time
import sys
import json
import os

# 将搜索目录改为上一级目录
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir))

from src.scripts.util.Util import Util
from src.scripts.util.DDSUtil import DDSUtil


"""
DDS相关函数
"""
DDSUtil.loadIdl(
    f"{os.path.dirname(os.path.abspath(__file__))}/../example/idl/example.idl"
)
DDSUtil.generateIdlCMakeLists("example")
DDSUtil.compileIdl("example")

DDSUtil.loadDDS(
    f"{os.path.dirname(os.path.abspath(__file__))}/../example/communication/dds_publisher_formal_demo.cpp"
)
DDSUtil.generateDDSCMakeLists("dds_publisher_formal_demo", ["example"])
DDSUtil.compileDDS("dds_publisher_formal_demo")


exit(1)

Util.compile_idl("src/idl/example.idl")
Util.compile_dds("server_src/dds_publisher_formal_demo.cpp")
Util.compileClientDemo(
    service_list=["atomic_service_mbsb", "atomic_service_sf"],
    topic_list=["example"],
    filename="client_formal_demo_with_dds.cpp",
)
Util.compileServerDemo(
    service_list=["atomic_service_mbsb", "atomic_service_sf"],
    filename="serverA_sync_server",
)
