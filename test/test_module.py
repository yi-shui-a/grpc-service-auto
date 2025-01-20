import time
import sys
import json
import os

from src.scripts.ServiceUtil import ServiceUtil
from src.scripts.GrpcServiceMethodUtil import GrpcServiceMethodUtil
from src.scripts.ServerUtil import ServerUtil
from src.scripts.Server import Server
from src.scripts.Util import Util

if __name__ == "__main__":

    serviceUtilsA = ServiceUtil()
    serviceUtilsB = ServiceUtil()
    # start = time.time()
    serviceUtilsA.parseHpp(
        f"{os.path.dirname(os.path.abspath(__file__))}/input_include/atomic_service_mbsb.h"
    )
    serviceUtilsB.parseHpp(
        f"{os.path.dirname(os.path.abspath(__file__))}/input_include/atomic_service_sf.h"
    )
    # end1 = time.time()
    serviceUtilsA.parseCpp(
        f"{os.path.dirname(os.path.abspath(__file__))}/input_src/atomic_service_mbsb.cpp"
    )
    serviceUtilsB.parseCpp(
        f"{os.path.dirname(os.path.abspath(__file__))}/input_src/atomic_service_sf.c"
    )
    # end2 = time.time()

    # print(".h parse time: ",(end1-start)*1000/2)
    # print(".cpp parse time: ",(end2-end1)*1000/2)

    methodUtilsA = GrpcServiceMethodUtil()
    methodUtilsB = GrpcServiceMethodUtil()
    methodUtilsA.set_service_method_util(serviceUtilsA._service)
    methodUtilsB.set_service_method_util(serviceUtilsB._service)
    methodUtilsA.generateProtoFile()
    methodUtilsB.generateProtoFile()
    methodUtilsA.generateServerImpl()
    methodUtilsB.generateServerImpl()
    methodUtilsA.generateStubImpl()
    methodUtilsB.generateStubImpl()
    methodUtilsA.add_info_to_json()
    methodUtilsB.add_info_to_json()
    methodUtilsA.generateGrpcFile()
    methodUtilsB.generateGrpcFile()

    # 创建一个server
    serverA = Server()
    with open(
        f"{os.path.dirname(os.path.abspath(__file__))}/user_info.json", "r"
    ) as file:
        user_info = json.loads(file.read())
    serverA.set_info_from_user(user_info)
    serverA.saveServerJson()
    serverUtilA = ServerUtil(serverA)
    # serverUtilA.compileDemo(filename="time_test")
    serverUtilA.generateSyncServer()
    serverUtilA.compileSyncServer()
