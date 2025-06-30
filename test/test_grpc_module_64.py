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
        f"{os.path.dirname(os.path.abspath(__file__))}/../example/grpc_example_64/atomic_show_cgsj/atomic_show_cgsj.h"
    )
    serviceB = AtomServiceUtil.parseHpp(
        f"{os.path.dirname(os.path.abspath(__file__))}/../example/grpc_example_64/atomic_show_ddpc/atomic_show_ddpc.h"
    )
    serviceC = AtomServiceUtil.parseHpp(
        f"{os.path.dirname(os.path.abspath(__file__))}/../example/grpc_example_64/atomic_show_ddzt/atomic_show_ddzt.h"
    )
    serviceD = AtomServiceUtil.parseHpp(
        f"{os.path.dirname(os.path.abspath(__file__))}/../example/grpc_example_64/atomic_show_hjrd/atomic_show_hjrd.h"
    )
    serviceE = AtomServiceUtil.parseHpp(
        f"{os.path.dirname(os.path.abspath(__file__))}/../example/grpc_example_64/atomic_show_sjrh/atomic_show_sjrh.h"
    )
    serviceF = AtomServiceUtil.parseHpp(
        f"{os.path.dirname(os.path.abspath(__file__))}/../example/grpc_example_64/atomic_show_ycl/atomic_show_ycl.h"
    )
    serviceG = AtomServiceUtil.parseHpp(
        f"{os.path.dirname(os.path.abspath(__file__))}/../example/grpc_example_64/atomic_show_ysdd/atomic_show_ysdd.h"
    )
    serviceH = AtomServiceUtil.parseHpp(
        f"{os.path.dirname(os.path.abspath(__file__))}/../example/grpc_example_64/atomic_show_zlsc/atomic_show_zlsc.h"
    )
    serviceI = AtomServiceUtil.parseHpp(
        f"{os.path.dirname(os.path.abspath(__file__))}/../example/grpc_example_64/atomic_show_ztjs/atomic_show_ztjs.h"
    )
    serviceJ = AtomServiceUtil.parseHpp(
        f"{os.path.dirname(os.path.abspath(__file__))}/../example/grpc_example_64/atomic_show_zxzl/atomic_show_zxzl.h"
    )
    
    # 解析 cpp 文件
    AtomServiceUtil.parseCpp(
        serviceA,
        f"{os.path.dirname(os.path.abspath(__file__))}/../example/grpc_example_64/atomic_show_cgsj/atomic_show_cgsj.cpp",
    )
    AtomServiceUtil.parseCpp(
        serviceB,
        f"{os.path.dirname(os.path.abspath(__file__))}/../example/grpc_example_64/atomic_show_ddpc/atomic_show_ddpc.cpp",
    )
    AtomServiceUtil.parseCpp(
        serviceC,
        f"{os.path.dirname(os.path.abspath(__file__))}/../example/grpc_example_64/atomic_show_ddzt/atomic_show_ddzt.cpp",
    )
    AtomServiceUtil.parseCpp(
        serviceD,
        f"{os.path.dirname(os.path.abspath(__file__))}/../example/grpc_example_64/atomic_show_hjrd/atomic_show_hjrd.cpp",
    )
    AtomServiceUtil.parseCpp(
        serviceE,
        f"{os.path.dirname(os.path.abspath(__file__))}/../example/grpc_example_64/atomic_show_sjrh/atomic_show_sjrh.cpp",
    )
    AtomServiceUtil.parseCpp(
        serviceF,
        f"{os.path.dirname(os.path.abspath(__file__))}/../example/grpc_example_64/atomic_show_ycl/atomic_show_ycl.cpp",
    )
    AtomServiceUtil.parseCpp(
        serviceG,
        f"{os.path.dirname(os.path.abspath(__file__))}/../example/grpc_example_64/atomic_show_ysdd/atomic_show_ysdd.cpp",
    )
    AtomServiceUtil.parseCpp(
        serviceH,
        f"{os.path.dirname(os.path.abspath(__file__))}/../example/grpc_example_64/atomic_show_zlsc/atomic_show_zlsc.cpp",
    )
    AtomServiceUtil.parseCpp(
        serviceI,
        f"{os.path.dirname(os.path.abspath(__file__))}/../example/grpc_example_64/atomic_show_ztjs/atomic_show_ztjs.cpp",
    )
    AtomServiceUtil.parseCpp(
        serviceJ,
        f"{os.path.dirname(os.path.abspath(__file__))}/../example/grpc_example_64/atomic_show_zxzl/atomic_show_zxzl.cpp",
    )

    process(serviceA)
    process(serviceB)
    process(serviceC)
    process(serviceD)
    process(serviceE)
    process(serviceF)
    process(serviceG)
    process(serviceH)
    process(serviceI)
    process(serviceJ)