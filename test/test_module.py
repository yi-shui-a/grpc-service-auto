import time
import sys
import json
import os

# 将搜索目录改为上一级目录
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir))

# from src.scripts.util.AtomServiceUtil import AtomServiceUtil
# from src.scripts.util.GrpcMethodUtil import GrpcMethodUtil
# from src.scripts.util.ServerUtil import ServerUtil
# from scripts.entity.Server import Server
# from src.scripts.util.Util import Util
# from src.scripts.util.DDSUtil import DDSUtil

from src.scripts.util import *
from src.scripts.entity import *

if __name__ == "__main__":

    """
    atomic_service相关的函数
    """
    # 解析h文件，生成service对象
    serviceA = AtomServiceUtil.parseHpp(
        f"{os.path.dirname(os.path.abspath(__file__))}/../example/mbsb/atomic_service_mbsb.h"
    )
    serviceB = AtomServiceUtil.parseHpp(
        f"{os.path.dirname(os.path.abspath(__file__))}/../example/sf/atomic_service_sf.h"
    )
    # 解析 cpp 文件
    AtomServiceUtil.parseCpp(
        serviceA,
        f"{os.path.dirname(os.path.abspath(__file__))}/../example/mbsb/atomic_service_mbsb.cpp",
    )
    AtomServiceUtil.parseCpp(
        serviceB,
        f"{os.path.dirname(os.path.abspath(__file__))}/../example/sf/atomic_service_sf.c",
    )

    # 生成微服务编译的cmake
    AtomServiceUtil.generateAtomServiceCMakeLists(serviceA)
    AtomServiceUtil.generateAtomServiceCMakeLists(serviceB)

    # proto生成编译相关函数
    GrpcMethodUtil.generateProtoFile(serviceA)
    GrpcMethodUtil.generateProtoFile(serviceB)

    GrpcMethodUtil.generateProtoCmakeLists(serviceA)
    GrpcMethodUtil.generateProtoCmakeLists(serviceB)

    GrpcMethodUtil.compileProtoFile(serviceA)
    GrpcMethodUtil.compileProtoFile(serviceB)

    # ServerImpl 生成编译相关函数
    GrpcMethodUtil.generateServerImpl(serviceA)
    GrpcMethodUtil.generateServerImpl(serviceB)

    GrpcMethodUtil.generateServerImplCMakeLists(serviceA)
    GrpcMethodUtil.generateServerImplCMakeLists(serviceB)

    GrpcMethodUtil.compileServerImpl(serviceA)
    GrpcMethodUtil.compileServerImpl(serviceB)

    # ClientImpl 生成编译相关函数
    GrpcMethodUtil.generateStubImpl(serviceA)
    GrpcMethodUtil.generateStubImpl(serviceB)

    GrpcMethodUtil.generateClientImplCMakeLists(serviceA)
    GrpcMethodUtil.generateClientImplCMakeLists(serviceB)

    GrpcMethodUtil.compileClientImpl(serviceA)
    GrpcMethodUtil.compileClientImpl(serviceB)

    # 将grpc的信息写入json
    GrpcMethodUtil.add_info_to_json(serviceA)
    GrpcMethodUtil.add_info_to_json(serviceB)

    """
    server相关函数
    """
    # 实例化一个server
    serverB = Server()
    with open(
        f"{os.path.dirname(os.path.abspath(__file__))}/user_info.json", "r"
    ) as file:
        user_info = json.loads(file.read())
    serverB.set_info_from_user(user_info)
    ServerUtil.saveServerJson(serverB)

    # SyncServer生成编译相关函数
    ServerUtil.generateSyncServer(serverB)
    ServerUtil.generateSyncServerCMakeLists(serverB)
    ServerUtil.compileSyncServer(serverB)
