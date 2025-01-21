from jinja2 import Template
import sys
import os
import re
import json
import subprocess

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir))
from ServiceMethod import ServiceMethod
from entity.OperatingSystem import OperatingSystem
from AtomService import AtomService
from entity.Message import Message
from config.types import cpp_types


class GrpcMethodUtil:
    def __init__(self):
        self.__service_name: str = None
        self.__operating_system: OperatingSystem = None
        self._service_methods: ServiceMethod = None
        self._messages: Message = None
        self.__language: str = ""

    def set_service_method_util(self, service: AtomService):
        self.__service_name = service._base_info.get_name()
        self.__operating_system = service._operating_systems
        self._service_methods = service._service_methods
        self._messages = service._messages
        self._generate_info()

    def _check_situation(self) -> bool:
        if (
            self.__service_name == None
            or self.__operating_system == None
            or self._service_methods == None
            or self._messages == None
        ):
            return False
        return True

    def _generate_info(self):
        self.__service_name_service = self.__service_name + "_Service"
        self.__service_name_package = self.__service_name + "_Package"
        self.__service_name_interface = self.__service_name + "_interface"

    def add_info_to_json(self):
        file_path = f"{os.path.dirname(os.path.abspath(__file__))}/../../atom_json/{self.__service_name}.json"
        try:
            # 检查文件是否存在
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")

            # 打开并读取 JSON 文件
            with open(file_path, "r") as file:
                data = json.load(file)
        except FileNotFoundError as e:
            print(f"Error: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return None
        data["grpc_info"] = {}
        data["grpc_info"]["name"] = self.__service_name
        data["grpc_info"]["description"] = ""
        data["grpc_info"]["name_package"] = self.__service_name_package
        data["grpc_info"]["name_service"] = self.__service_name_service
        # data["grpc_info"]["name_interface"] = self.__service_name_interface

        with open(
            f"{os.path.dirname(os.path.abspath(__file__))}/../../atom_json/{self.__service_name}.json",
            "w",
        ) as file:
            file.write(json.dumps(data, indent=4))
        print(
            f"add grpc info to {os.path.dirname(os.path.abspath(__file__))}/../../atom_json/{self.__service_name}.json successfully!"
        )

    def generateProtoFile(self):
        # TODO: Read the input file and extract the necessary information
        # Example: Read from inputFilrName and write to outputFilrName
        # 定义模板
        proto_template = Template(
            open(
                f"{os.path.dirname(os.path.abspath(__file__))}/../../src/templates/proto_template.j2"
            ).read()
        )

        res_str = proto_template.render(
            service_name_package=self.__service_name_package,
            service_name_service=self.__service_name_service,
            messages=self._messages,
            methods=self._service_methods,
        )

        # 确保目录存在
        os.makedirs(
            f"{os.path.dirname(os.path.abspath(__file__))}/../../protos/",
            exist_ok=True,
        )

        # 将res_str写入框架内的cpp文件中，同名不同路径
        with open(
            f"{os.path.dirname(os.path.abspath(__file__))}/../../protos/{self.__service_name}.proto",
            "w",
        ) as file:
            file.write(res_str)
        print(
            f"{os.path.dirname(os.path.abspath(__file__))}/../../protos/{self.__service_name}.proto generated successfully!"
        )

    def generateGrpcFile(self):
        # 定义make命令及其参数
        make_command = [
            "make",
            "-C",
            f"{os.path.dirname(os.path.abspath(__file__))}/make/",
            "-f",
            "proto_make",
            f"PROTO={self.__service_name}.proto",
        ]
        try:
            # 调用make命令，并等待其完成
            result = subprocess.run(
                make_command,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )

            # 如果make命令成功执行，则打印其输出
            if result.stdout:
                print("Make Output:\n", result.stdout)

        except subprocess.CalledProcessError as e:
            # 如果make命令失败，则捕获异常并打印错误信息
            print("Make failed with error:", e)
            print("Error Output:\n", e.stderr)

    def generateLibFile(self, inputFilrName, outputFilrName):
        # TODO: Read the input file and extract the necessary information
        # Example: Read from inputFilrName and write to outputFilrName
        pass

    def generateServerImpl(self):
        # TODO: Read the input file and extract the necessary information
        # Example: Read from inputFilrName and write to outputFilr
        proto_template = Template(
            open(
                f"{os.path.dirname(os.path.abspath(__file__))}/../../src/templates/server_impl_template.j2"
            ).read()
        )

        res_str = proto_template.render(
            service_name=self.__service_name,
            service_name_package=self.__service_name_package,
            service_name_service=self.__service_name_service,
            service_name_interface=self.__service_name_interface,
            messages=self._messages,
            methods=self._service_methods,
        )

        # 确保目录存在
        os.makedirs(
            f"{os.path.dirname(os.path.abspath(__file__))}/../../rpc_server_inc/",
            exist_ok=True,
        )

        # 将res_str写入框架内的cpp文件中，同名不同路径
        with open(
            f"{os.path.dirname(os.path.abspath(__file__))}/../../rpc_server_inc/{self.__service_name}_impl.h",
            "w",
        ) as file:
            file.write(res_str)
        print(
            f"{os.path.dirname(os.path.abspath(__file__))}/../../rpc_server_inc/{self.__service_name}_impl.h generated successfully!"
        )

    def generateStubImpl(self):
        # TODO: Read the input file and extract the necessary information
        # Example: Read from inputFilrName and write to outputFilr
        proto_template = Template(
            open(
                f"{os.path.dirname(os.path.abspath(__file__))}/../../src/templates/client_impl_template.j2"
            ).read()
        )

        res_str = proto_template.render(
            service_name=self.__service_name,
            service_name_package=self.__service_name_package,
            service_name_service=self.__service_name_service,
            service_name_interface=self.__service_name_interface,
            messages=self._messages,
            methods=self._service_methods,
        )

        # 确保目录存在
        os.makedirs(
            f"{os.path.dirname(os.path.abspath(__file__))}/../../rpc_client_inc/",
            exist_ok=True,
        )

        # 将res_str写入框架内的cpp文件中，同名不同路径
        with open(
            f"{os.path.dirname(os.path.abspath(__file__))}/../../rpc_client_inc/{self.__service_name}_client.h",
            "w",
        ) as file:
            file.write(res_str)
        print(
            f"{os.path.dirname(os.path.abspath(__file__))}/../../rpc_client_inc/{self.__service_name}_client.h generated successfully!"
        )
