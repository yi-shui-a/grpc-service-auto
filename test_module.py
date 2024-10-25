from src.utils.ServiceUtil import ServiceUtil
from src.utils.GrpcServiceMethodUtil import GrpcServiceMethodUtil

if __name__ == '__main__':

    serviceUtilsA = ServiceUtil()
    serviceUtilsB = ServiceUtil()

    serviceUtilsA.parseHpp("/root/grpc-generate-server/input_inc/atomic_service_mbsb.h")
    serviceUtilsA.parseCpp("/root/grpc-generate-server/input_src/atomic_service_mbsb.cpp")
    serviceUtilsB.parseHpp("/root/grpc-generate-server/input_inc/atomic_service_sf.h")
    serviceUtilsB.parseCpp("/root/grpc-generate-server/input_src/atomic_service_sf.c")
    
    methodUtilsA = GrpcServiceMethodUtil()
    methodUtilsB = GrpcServiceMethodUtil()
    methodUtilsA.set_service_method_util(serviceUtilsA._service)
    methodUtilsB.set_service_method_util(serviceUtilsB._service)
    methodUtilsA.generateProtoFile()
    methodUtilsB.generateProtoFile()