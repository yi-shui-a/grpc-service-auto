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
解析输入文件，生成编译源服务的cmakelist
"""
if __name__ == "__main__":
    # 解析h文件，生成service对象
    mbsb_service = AtomServiceUtil.parseHpp(
        f"{os.path.dirname(os.path.abspath(__file__))}/../../example/grpc_example/mbsb/atomic_service_mbsb.h"
    )
    sf_service = AtomServiceUtil.parseHpp(
        f"{os.path.dirname(os.path.abspath(__file__))}/../../example/grpc_example/sf/atomic_service_sf.h"
    )
    # 解析 cpp 文件
    AtomServiceUtil.parseCpp(
        mbsb_service,
        f"{os.path.dirname(os.path.abspath(__file__))}/../../example/grpc_example/mbsb/atomic_service_mbsb.cpp",
    )
    AtomServiceUtil.parseCpp(
        sf_service,
        f"{os.path.dirname(os.path.abspath(__file__))}/../../example/grpc_example/sf/atomic_service_sf.c",
    )

    # 生成编译源服务的cmakelist
    AtomServiceUtil.generateAtomServiceCMakeLists(mbsb_service)
    AtomServiceUtil.generateAtomServiceCMakeLists(sf_service)

    # 将grpc的信息写入json
    GrpcMethodUtil.add_info_to_json(mbsb_service)
    GrpcMethodUtil.add_info_to_json(sf_service)
