import time

from src.utils.ServiceUtil import ServiceUtil
from src.utils.GrpcServiceMethodUtil import GrpcServiceMethodUtil

if __name__ == '__main__':

    serviceUtilsA = ServiceUtil()
    serviceUtilsB = ServiceUtil()
    # start = time.time()
    serviceUtilsA.parseHpp("/root/grpc-generate-server/input_inc/atomic_service_mbsb.h")
    serviceUtilsB.parseHpp("/root/grpc-generate-server/input_inc/atomic_service_sf.h")
    # end1 = time.time()
    serviceUtilsA.parseCpp("/root/grpc-generate-server/input_src/atomic_service_mbsb.cpp")
    serviceUtilsB.parseCpp("/root/grpc-generate-server/input_src/atomic_service_sf.c")
    # end2 = time.time()
    
    # print(".h parse time: ",(end1-start)*1000/2)
    # print(".cpp parse time: ",(end2-end1)*1000/2)
    
    methodUtilsA = GrpcServiceMethodUtil()
    methodUtilsB = GrpcServiceMethodUtil()
    methodUtilsA.set_service_method_util(serviceUtilsA._service)
    methodUtilsB.set_service_method_util(serviceUtilsB._service)
    methodUtilsA.generateProtoFile()
    methodUtilsB.generateProtoFile()