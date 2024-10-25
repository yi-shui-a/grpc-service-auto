import os
from src.utils.ServiceUtil import ServiceUtils

from  Jinja2 import Services2Server 

if __name__ == "__main__":
    # 第一步，生成原子服务的json
    print(">>>>[INFO]  parse cpp and hpp  <<<")
    serviceUtilsA = ServiceUtils()
    serviceUtilsB = ServiceUtils()
    # serviceUtils.parseHpp("test/atom_service_mbsb.h")
    # serviceUtils.parseHpp("D:\ZT\长安望江_服务化\code_demo\grpc-generate-server\\test\\atom_service_mbsb.h")
    # print("\n\n\n\n")
    # print(json.dumps(serviceUtils._service.to_dict(), indent=4))
    serviceUtilsA.parseHpp("/root/grpc-generate-server/input_inc/atom_service_mbsb.h")
    serviceUtilsA.parseCpp("/root/grpc-generate-server/input_src/atom_service_mbsb.c")
    serviceUtilsB.parseHpp("/root/grpc-generate-server/input_inc/sf.h")
    serviceUtilsB.parseCpp("/root/grpc-generate-server/input_src/sf.c")
    

    # 第二步，加载service_info.json
    ServerBaseInfo_json_file = os.path.abspath("./server_info.json")
    # TODO: Step1 ServerBaseInfo.json config info to genCode
    server_name, services_name =  Services2Server.main(ServerBaseInfo_json_file)