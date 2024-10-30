from jinja2 import Template
import sys
import os
import re

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
import ServiceMethod
import OperatingSystem
import AtomService
import Message
from config.types import cpp_types
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
        self.__service_name_service = self.__service_name + "_Service"
        self.__service_name_package = self.__service_name +"_Package"
        self.__service_name_interface = self.__service_name +"_interface"
        
    def _type_convert(self):
        # 修改数据类型
        # 删除std::
        for message in self._messages:
            for field in message._fields:
                # field._type_proto为赋值时，才进行此操作
                if field._type_proto !="":
                    continue
                
                # 为 _type_proto 赋值
                field._type_proto = cpp_types.get(field._type,field._type)
                # 去除命名空间标示符
                if field._type_proto.count("std::") > 0:
                    field._type_proto = field._type_proto.replace("std::", "")
                    
                # 数组转为repeated 
                # vector
                if field._type_proto.count("vector") > 0:
                    field._repeated = True
                    # 使用正则表达式提取类型
                    match = re.search(r'vector<(\w+)>', field._type_proto)
                    temp_str = cpp_types.get(match.group(1),match.group(1))
                    if match:
                        field._type_proto = "repeated " +  temp_str
                        
                            
                # []
                if field._name.count('[') > 0 and field._name.count(']') > 0:
                    field._repeated = True
                    field._type_proto =  "repeated " + field._type_proto
                    
                    
                # map中的数据类型处理
                if field._type_proto.count("map") > 0:
                    field._map = True
                    match = re.search(r'map<(\w+),\s*(\w+)>', field._type_proto)
                    if match:
                        field._key = cpp_types.get(match.group(1),match.group(1))
                        field._value = cpp_types.get(match.group(2),match.group(2))
                        field._type_proto = f"map<{field._key}, {field._value}>"
                
                
    def generateProtoFile(self):
        # TODO: Read the input file and extract the necessary information
        # Example: Read from inputFilrName and write to outputFilrName
        # 定义模板
        proto_template = Template(open(f"{os.path.dirname(os.path.abspath(__file__))}/../../Jinja2/proto_template.j2").read())
        
        
        res_str = proto_template.render(service_name_package = self.__service_name_package, service_name_service = self.__service_name_service, messages = self._messages, methods = self._service_methods)
        
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
    
    def generateServerImpl(self):
        # TODO: Read the input file and extract the necessary information
        # Example: Read from inputFilrName and write to outputFilr
        proto_template = Template(open(f"{os.path.dirname(os.path.abspath(__file__))}/../../Jinja2/server_impl_template.j2").read())

        res_str = proto_template.render(service_name = self.__service_name, service_name_package = self.__service_name_package, service_name_service = self.__service_name_service, service_name_interface=self.__service_name_interface, messages = self._messages, methods = self._service_methods)
        
        # 将res_str写入框架内的cpp文件中，同名不同路径
        with open(f"{os.path.dirname(os.path.abspath(__file__))}/../../rpc_server_inc/{self.__service_name}_impl.h", 'w') as file:
            file.write(res_str)
        print(f"{os.path.dirname(os.path.abspath(__file__))}/../../rpc_server_inc/{self.__service_name}_impl.h generated successfully!")

    def generateStubImpl(self):
        # TODO: Read the input file and extract the necessary information
        # Example: Read from inputFilrName and write to outputFilr
        proto_template = Template(open(f"{os.path.dirname(os.path.abspath(__file__))}/../../Jinja2/client_impl_template.j2").read())

        res_str = proto_template.render(service_name = self.__service_name, service_name_package = self.__service_name_package, service_name_service = self.__service_name_service, service_name_interface=self.__service_name_interface, messages = self._messages, methods = self._service_methods)
        
        # 将res_str写入框架内的cpp文件中，同名不同路径
        with open(f"{os.path.dirname(os.path.abspath(__file__))}/../../rpc_client_inc/{self.__service_name}_client.h", 'w') as file:
            file.write(res_str)
        print(f"{os.path.dirname(os.path.abspath(__file__))}/../../rpc_client_inc/{self.__service_name}_client.h generated successfully!")