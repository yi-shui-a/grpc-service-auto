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
根据解析的信息生成proto文件并编译
"""
if __name__ == "__main__":
    # 加载AtomService
    # 读取文件内容
    mbsb_service = AtomServiceUtil.loadAtomService(
        f"{os.path.dirname(os.path.abspath(__file__))}/../../db/atomic_service/atomic_service_mbsb/atomic_service_mbsb.json"
    )
    sf_service = AtomServiceUtil.loadAtomService(
        f"{os.path.dirname(os.path.abspath(__file__))}/../../db/atomic_service/atomic_service_sf/atomic_service_sf.json"
    )

    # 根据解析的信息生成proto文件
    GrpcMethodUtil.generateProtoFile(mbsb_service)
    GrpcMethodUtil.generateProtoFile(sf_service)

    # 根据解析的信息生成proto文件的cmakeList
    GrpcMethodUtil.generateProtoCmakeLists(mbsb_service)
    GrpcMethodUtil.generateProtoCmakeLists(sf_service)

    # 编译proto文件
    GrpcMethodUtil.compileProtoFile(mbsb_service)
    GrpcMethodUtil.compileProtoFile(sf_service)
