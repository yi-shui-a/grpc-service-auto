from jinja2 import Template
import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
import ServiceMethod
import OperatingSystem
import AtomService
import Message
from config.types import cpp_types

class GrpcServiceMethodUtil:
    def __init__(self):
        self.__service_name:str = None 
        self.__operating_system:OperatingSystem.OperatingSystem = None
        self._service_methods:ServiceMethod.ServiceMethod = None
        self._messages:Message.Message = None
        self.__language = ""
        
    def set_service_method_util(self,service:AtomService.AtomService):
        self.__service_name = service._base_info.getName()
        self.__operating_system = service._operating_systems
        self._service_methods = service._service_methods
        self._messages = service._messages
        self._generate_info()
        self._type_convert()
        
        
    def _check_situation(self)->bool:
        if self.__service_name==None or self.__operating_system == None or self._service_methods == None or self._messages == None :
            return False
        return True
    
    def _generate_info(self):
        self.__service_name_proto = self.__service_name + "_service"
        self.__service_name_package = self.__service_name +"_package"
        
    def _type_convert(self):
        # 修改数据类型
        # 删除std::
        for message in self._messages:
            for field in message._fields:
                    field._type = cpp_types.get(field._type,field._type)
                    if field._type.count("std::") > 0:
                        field._type = field._type.replace("std::", "")
                    
        
            

    def generateProtoFile(self):
        # TODO: Read the input file and extract the necessary information
        # Example: Read from inputFilrName and write to outputFilrName
        # 定义模板
        proto_template = Template(open(f"{os.path.dirname(os.path.abspath(__file__))}/../../Jinja2/proto_template.j2").read())
        
        
        res_str = proto_template.render(service_name_package = self.__service_name_package, service_name_proto = self.__service_name_proto, messages = self._messages, methods = self._service_methods)
        
        # 将res_str写入框架内的cpp文件中，同名不同路径
        with open(f"{os.path.dirname(os.path.abspath(__file__))}/../../protos/{self.__service_name}.proto", 'w') as file:
            file.write(res_str)
        print(f"{os.path.dirname(os.path.abspath(__file__))}/../../protos/{self.__service_name}.proto generated successfully!")
        
        pass
    def generateGrpcFile(self, inputFilrName, outputFilrName):
        # TODO: Read the input file and extract the necessary information
        # Example: Read from inputFilrName and write to outputFilrName
        pass

    def generateLibFile(self, inputFilrName, outputFilrName):
        # TODO: Read the input file and extract the necessary information
        # Example: Read from inputFilrName and write to outputFilrName
        pass
    def generateServerImpl(self, inputFilrName, outputFileName):
        # TODO: Read the input file and extract the necessary information
        # Example: Read from inputFilrName and write to outputFilr
        pass
    def generateStubImpl(self, inputFilrName, outputFileName):
        # TODO: Read the input file and extract the necessary information
        # Example: Read from inputFilrName and write to outputFilr
        pass