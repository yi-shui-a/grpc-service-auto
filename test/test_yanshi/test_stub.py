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
根据解析的信息生成client_stub文件并编译
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

    # 生成 ClientImpl 代码
    GrpcMethodUtil.generateStubImpl(mbsb_service)
    GrpcMethodUtil.generateStubImpl(sf_service)

    # 生成编译 ClientImpl 的 cmake
    GrpcMethodUtil.generateClientImplCMakeLists(mbsb_service)
    GrpcMethodUtil.generateClientImplCMakeLists(sf_service)

    # 编译 ClientImpl
    GrpcMethodUtil.compileClientImpl(mbsb_service)
    GrpcMethodUtil.compileClientImpl(sf_service)
