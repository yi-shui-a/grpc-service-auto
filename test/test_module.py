import time
import sys
import json
import os

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir))

from src.scripts.util.AtomServiceUtil import AtomServiceUtil
from src.scripts.util.GrpcMethodUtil import GrpcMethodUtil
from src.scripts.util.ServerUtil import ServerUtil
from src.scripts.Server import Server
from src.scripts.util.Util import Util

if __name__ == "__main__":
    serviceA = AtomServiceUtil.parseHpp(
        f"{os.path.dirname(os.path.abspath(__file__))}/../example/mbsb/atomic_service_mbsb.h"
    )
    serviceB = AtomServiceUtil.parseHpp(
        f"{os.path.dirname(os.path.abspath(__file__))}/../example/sf/atomic_service_sf.h"
    )
    AtomServiceUtil.parseCpp(
        serviceA,
        f"{os.path.dirname(os.path.abspath(__file__))}/../example/mbsb/atomic_service_mbsb.cpp",
    )
    AtomServiceUtil.parseCpp(
        serviceB,
        f"{os.path.dirname(os.path.abspath(__file__))}/../example/sf/atomic_service_sf.c",
    )

    GrpcMethodUtil.generateProtoFile(serviceA)
    GrpcMethodUtil.generateProtoFile(serviceB)

    GrpcMethodUtil.generateProtoCmakeLists(serviceA)
    GrpcMethodUtil.generateProtoCmakeLists(serviceB)

    GrpcMethodUtil.compileProtoFile(serviceA)
    GrpcMethodUtil.compileProtoFile(serviceB)

    GrpcMethodUtil.generateServerImpl(serviceA)
    GrpcMethodUtil.generateServerImpl(serviceB)

    GrpcMethodUtil.generateStubImpl(serviceA)
    GrpcMethodUtil.generateStubImpl(serviceB)

    exit(1)

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

    methodUtilsA = GrpcMethodUtil()
    methodUtilsB = GrpcMethodUtil()
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
