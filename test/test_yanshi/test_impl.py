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
根据解析的信息生成server_impl文件并编译
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

    #  生成ServerImpl代码
    GrpcMethodUtil.generateServerImpl(mbsb_service)
    GrpcMethodUtil.generateServerImpl(sf_service)

    # 生成编译ServerImpl的cmake
    GrpcMethodUtil.generateServerImplCMakeLists(mbsb_service)
    GrpcMethodUtil.generateServerImplCMakeLists(sf_service)

    # 编译ServerImpl
    GrpcMethodUtil.compileServerImpl(mbsb_service)
    GrpcMethodUtil.compileServerImpl(sf_service)
