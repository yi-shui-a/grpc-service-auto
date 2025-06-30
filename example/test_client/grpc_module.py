import time
import sys
import json
import os

# 将搜索目录改为上一级目录
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir,os.pardir))

# from src.scripts.util.AtomServiceUtil import AtomServiceUtil
# from src.scripts.util.GrpcMethodUtil import GrpcMethodUtil
# from src.scripts.util.ServerUtil import ServerUtil
# from scripts.entity.Server import Server
# from src.scripts.util.Util import Util
# from src.scripts.util.GrpcDDSUtil import GrpcDDSUtil

from src.scripts.util import *
from src.scripts.entity import *

def process(service:AtomService):
    
    # 生成微服务编译的cmake
    AtomServiceUtil.generateAtomServiceCMakeLists(service)

    # proto生成编译相关函数
    GrpcMethodUtil.generateProtoFile(service)
    GrpcMethodUtil.generateProtoCmakeLists(service)
    GrpcMethodUtil.compileProtoFile(service)

    # ServerImpl 生成编译相关函数
    GrpcMethodUtil.generateServerImpl(service)
    GrpcMethodUtil.generateServerImplCMakeLists(service)
    GrpcMethodUtil.compileServerImpl(service)

    # ClientImpl 生成编译相关函数
    GrpcMethodUtil.generateStubImpl(service)
    GrpcMethodUtil.generateClientImplCMakeLists(service)
    GrpcMethodUtil.compileClientImpl(service)
    # 将grpc的信息写入json
    GrpcMethodUtil.add_info_to_json(service)


if __name__ == "__main__":

    """
    atomic_service相关的函数
    """
    # 解析h文件，生成service对象
    serviceA = AtomServiceUtil.parseHpp(
        f"{os.path.dirname(os.path.abspath(__file__))}/atomic_test_fusion/atomic_test_fusion.h"
    )
    serviceB = AtomServiceUtil.parseHpp(
        f"{os.path.dirname(os.path.abspath(__file__))}/atomic_test_infrared/atomic_test_infrared.h"
    )
    serviceC = AtomServiceUtil.parseHpp(
        f"{os.path.dirname(os.path.abspath(__file__))}/atomic_test_light/atomic_test_light.h"
    )
    serviceD = AtomServiceUtil.parseHpp(
        f"{os.path.dirname(os.path.abspath(__file__))}/atomic_test_radar/atomic_test_radar.h"
    )
    serviceE = AtomServiceUtil.parseHpp(
        f"{os.path.dirname(os.path.abspath(__file__))}/atomic_test_zlsc/atomic_test_zlsc.h"
    )
    
    # 解析 cpp 文件
    AtomServiceUtil.parseCpp(
        serviceA,
        f"{os.path.dirname(os.path.abspath(__file__))}/atomic_test_fusion/atomic_test_fusion.cpp",
    )
    AtomServiceUtil.parseCpp(
        serviceB,
        f"{os.path.dirname(os.path.abspath(__file__))}/atomic_test_infrared/atomic_test_infrared.cpp",
    )
    AtomServiceUtil.parseCpp(
        serviceC,
        f"{os.path.dirname(os.path.abspath(__file__))}/atomic_test_light/atomic_test_light.cpp",
    )
    AtomServiceUtil.parseCpp(
        serviceD,
        f"{os.path.dirname(os.path.abspath(__file__))}/atomic_test_radar/atomic_test_radar.cpp",
    )
    AtomServiceUtil.parseCpp(
        serviceE,
        f"{os.path.dirname(os.path.abspath(__file__))}/atomic_test_zlsc/atomic_test_zlsc.cpp",
    )

    process(serviceA)
    process(serviceB)
    process(serviceC)
    process(serviceD)
    process(serviceE)
