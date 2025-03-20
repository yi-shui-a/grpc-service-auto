from jinja2 import Template
import sys
import os
import re
import json


sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir))
from ServiceMethod import ServiceMethod
from entity.OperatingSystem import OperatingSystem
from entity.Message import Message
from AtomService import AtomService

# from scripts.config.globals import cpp_types
from config import cpp_types
from util.Util import Util


class GrpcMethodUtil:
    grpc_service_name_suffix = "_Service"
    grpc_service_package_suffix = "_Package"
    grpc_service_interface_suffix = "_Interface"

    grpc_service_sync_server_impl_suffix = "_sync_server_impl"
    grpc_service_sync_client_impl_suffix = "_sync_client_impl"

    grpc_service_async_server_impl_suffix = "_async_server_impl"
    grpc_service_async_client_impl_suffix = "_async_client_impl"

    def __init__(self):
        pass
        # self.__service_name: str = None
        # self.__operating_system: OperatingSystem = None
        # self._service_methods: ServiceMethod = None
        # self._messages: Message = None
        # self.__language: str = ""

    @staticmethod
    def add_info_to_json(atom_service: AtomService):
        service_name = atom_service._base_info.get_name()
        file_path = f"{os.path.dirname(os.path.abspath(__file__))}/../../../db/atomic_service/{service_name}/{service_name}.json"
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
        data["grpc_info"]["name"] = service_name
        data["grpc_info"]["description"] = ""
        data["grpc_info"]["name_package"] = (
            service_name + GrpcMethodUtil.grpc_service_package_suffix
        )
        data["grpc_info"]["name_service"] = (
            service_name + GrpcMethodUtil.grpc_service_name_suffix
        )
        data["grpc_info"]["name_interface"] = (
            service_name + GrpcMethodUtil.grpc_service_interface_suffix
        )
        data["grpc_info"]["sync_server_impl"] = (
            service_name + GrpcMethodUtil.grpc_service_sync_server_impl_suffix
        )
        data["grpc_info"]["sync_client_impl"] = (
            service_name + GrpcMethodUtil.grpc_service_sync_client_impl_suffix
        )
        data["grpc_info"]["async_server_impl"] = (
            service_name + GrpcMethodUtil.grpc_service_async_server_impl_suffix
        )
        data["grpc_info"]["async_client_impl"] = (
            service_name + GrpcMethodUtil.grpc_service_async_client_impl_suffix
        )

        with open(
            f"{os.path.dirname(os.path.abspath(__file__))}/../../../db/atomic_service/{service_name}/{service_name}.json",
            "w",
        ) as file:
            file.write(json.dumps(data, indent=4))
        print(
            f"add grpc info to {os.path.dirname(os.path.abspath(__file__))}/../../../db/atomic_service/{service_name}/{service_name}.json successfully!"
        )

    @staticmethod
    def generateProtoFile(atom_service: AtomService):
        # TODO: Read the input file and extract the necessary information
        # Example: Read from inputFilrName and write to outputFilrName
        # 定义模板
        proto_template = Template(
            open(
                f"{os.path.dirname(os.path.abspath(__file__))}/../../templates/proto_process_template/proto_template.j2"
            ).read()
        )

        res_str = proto_template.render(
            grpc_service_package=atom_service._base_info.get_name()
            + GrpcMethodUtil.grpc_service_package_suffix,
            grpc_service_name=atom_service._base_info.get_name()
            + GrpcMethodUtil.grpc_service_name_suffix,
            messages=atom_service._messages,
            methods=atom_service._service_methods,
        )

        # 确保目录存在
        os.makedirs(
            f"{os.path.dirname(os.path.abspath(__file__))}/../../../db/atomic_service/{atom_service._base_info.get_name()}/protos/",
            exist_ok=True,
        )

        # 将res_str写入框架内的cpp文件中，同名不同路径
        with open(
            f"{os.path.dirname(os.path.abspath(__file__))}/../../../db/atomic_service/{atom_service._base_info.get_name()}/protos/{atom_service._base_info.get_name()}.proto",
            "w",
        ) as file:
            file.write(res_str)
        print(
            f"{os.path.dirname(os.path.abspath(__file__))}/../../../db/atomic_service/{atom_service._base_info.get_name()}/protos/{atom_service._base_info.get_name()}.proto generated successfully!"
        )

    @staticmethod
    def generateProtoCmakeLists(atom_service: AtomService):
        # 生成编译proto文件的cmakelist文件
        # 定义模板
        proto_template = Template(
            open(
                f"{os.path.dirname(os.path.abspath(__file__))}/../../templates/proto_process_template/proto_compile_cmake_template.j2"
            ).read()
        )
        res_str = proto_template.render(service_name=atom_service._base_info.get_name())

        # 确保目录存在
        os.makedirs(
            f"{os.path.dirname(os.path.abspath(__file__))}/../../../db/atomic_service/{atom_service._base_info.get_name()}/protos/",
            exist_ok=True,
        )

        # 将res_str写入框架内的cpp文件中，同名不同路径
        with open(
            f"{os.path.dirname(os.path.abspath(__file__))}/../../../db/atomic_service/{atom_service._base_info.get_name()}/protos/CMakeLists.txt",
            "w",
        ) as file:
            file.write(res_str)
        print(
            f"{os.path.dirname(os.path.abspath(__file__))}/../../../db/atomic_service/{atom_service._base_info.get_name()}/protos/CMakeLists.txt generated successfully!"
        )

    @staticmethod
    def compileProtoFile(atom_service: AtomService):
        """
        自动生成 Protobuf 和 gRPC 文件的 Python 函数。

        :param proto_dir: .proto 文件所在的目录路径
        """
        service_name = atom_service._base_info.get_name()
        proto_dir = f"{os.path.dirname(os.path.abspath(__file__))}/../../../db/atomic_service/{atom_service._base_info.get_name()}/protos/"

        Util.compileCmakeProject(proto_dir, service_name, file_type="proto")

    @staticmethod
    def generateServerImpl(atom_service: AtomService):
        # TODO: Read the input file and extract the necessary information
        # Example: Read from inputFilrName and write to outputFilr
        service_name = atom_service._base_info.get_name()
        proto_template = Template(
            open(
                f"{os.path.dirname(os.path.abspath(__file__))}/../../templates/sync_impl_process_template/sync_server_impl_template.j2"
            ).read()
        )

        res_str = proto_template.render(
            service_name=service_name,
            service_name_package=service_name
            + GrpcMethodUtil.grpc_service_package_suffix,
            service_name_service=service_name + GrpcMethodUtil.grpc_service_name_suffix,
            service_name_interface=service_name
            + GrpcMethodUtil.grpc_service_interface_suffix,
            messages=atom_service._messages,
            methods=atom_service._service_methods,
        )

        # 确保目录存在
        os.makedirs(
            f"{os.path.dirname(os.path.abspath(__file__))}/../../../db/atomic_service/{service_name}/sync_server_impl/",
            exist_ok=True,
        )

        # 将res_str写入框架内的cpp文件中，同名不同路径
        with open(
            f"{os.path.dirname(os.path.abspath(__file__))}/../../../db/atomic_service/{service_name}/sync_server_impl/{service_name + GrpcMethodUtil.grpc_service_sync_server_impl_suffix}.cpp",
            "w",
        ) as file:
            file.write(res_str)
        print(
            f"{os.path.dirname(os.path.abspath(__file__))}/../../../db/atomic_service/{service_name}/sync_server_impl/{service_name + GrpcMethodUtil.grpc_service_sync_server_impl_suffix}.cpp generated successfully!"
        )

    @staticmethod
    def generateServerImplCMakeLists(atom_service: AtomService):
        service_name = atom_service._base_info.get_name()
        proto_template = Template(
            open(
                f"{os.path.dirname(os.path.abspath(__file__))}/../../templates/sync_impl_process_template/sync_server_impl_compile_cmake_template.j2"
            ).read()
        )
        res_str = proto_template.render(
            project_name=service_name
            + GrpcMethodUtil.grpc_service_sync_server_impl_suffix,
            service_name=service_name,
        )

        # 确保目录存在
        os.makedirs(
            f"{os.path.dirname(os.path.abspath(__file__))}/../../../db/atomic_service/{service_name}/sync_server_impl/",
            exist_ok=True,
        )

        # 将res_str写入框架内的cpp文件中，同名不同路径
        with open(
            f"{os.path.dirname(os.path.abspath(__file__))}/../../../db/atomic_service/{service_name}/sync_server_impl/CMakeLists.txt",
            "w",
        ) as file:
            file.write(res_str)
        print(
            f"{os.path.dirname(os.path.abspath(__file__))}/../../../db/atomic_service/{service_name}/sync_server_impl/CMakeLists.txt generated successfully!"
        )

    @staticmethod
    def compileServerImpl(atom_service: AtomService):
        service_name = atom_service._base_info.get_name()
        server_impl_dir = f"{os.path.dirname(os.path.abspath(__file__))}/../../../db/atomic_service/{service_name}/sync_server_impl/"

        Util.compileCmakeProject(
            server_impl_dir,
            service_name + GrpcMethodUtil.grpc_service_sync_server_impl_suffix,
            file_type="cpp",
        )

    @staticmethod
    def generateStubImpl(atom_service: AtomService):
        # TODO: Read the input file and extract the necessary information
        # Example: Read from inputFilrName and write to outputFilr
        service_name = atom_service._base_info.get_name()
        proto_template = Template(
            open(
                f"{os.path.dirname(os.path.abspath(__file__))}/../../templates/sync_impl_process_template/sync_client_impl_template.j2"
            ).read()
        )

        res_str = proto_template.render(
            service_name=service_name,
            service_name_package=service_name
            + GrpcMethodUtil.grpc_service_package_suffix,
            service_name_service=service_name + GrpcMethodUtil.grpc_service_name_suffix,
            service_name_interface=service_name
            + GrpcMethodUtil.grpc_service_interface_suffix,
            messages=atom_service._messages,
            methods=atom_service._service_methods,
        )

        # 确保目录存在
        os.makedirs(
            f"{os.path.dirname(os.path.abspath(__file__))}/../../../db/atomic_service/{service_name}/sync_client_impl/",
            exist_ok=True,
        )

        # 将res_str写入框架内的cpp文件中，同名不同路径
        with open(
            f"{os.path.dirname(os.path.abspath(__file__))}/../../../db/atomic_service/{service_name}/sync_client_impl/{service_name + GrpcMethodUtil.grpc_service_sync_client_impl_suffix}.cpp",
            "w",
        ) as file:
            file.write(res_str)
        print(
            f"{os.path.dirname(os.path.abspath(__file__))}/../../../db/atomic_service/{service_name}/sync_client_impl/{service_name + GrpcMethodUtil.grpc_service_sync_client_impl_suffix}.cpp generated successfully!"
        )

    @staticmethod
    def generateClientImplCMakeLists(atom_service: AtomService):
        service_name = atom_service._base_info.get_name()
        proto_template = Template(
            open(
                f"{os.path.dirname(os.path.abspath(__file__))}/../../templates/sync_impl_process_template/sync_client_impl_compile_cmake_template.j2"
            ).read()
        )
        res_str = proto_template.render(
            project_name=service_name
            + GrpcMethodUtil.grpc_service_sync_client_impl_suffix,
            service_name=service_name,
        )

        # 确保目录存在
        os.makedirs(
            f"{os.path.dirname(os.path.abspath(__file__))}/../../../db/atomic_service/{service_name}/sync_client_impl/",
            exist_ok=True,
        )

        # 将res_str写入框架内的cpp文件中，同名不同路径
        with open(
            f"{os.path.dirname(os.path.abspath(__file__))}/../../../db/atomic_service/{service_name}/sync_client_impl/CMakeLists.txt",
            "w",
        ) as file:
            file.write(res_str)
        print(
            f"{os.path.dirname(os.path.abspath(__file__))}/../../../db/atomic_service/{service_name}/sync_client_impl/CMakeLists.txt generated successfully!"
        )

    @staticmethod
    def compileClientImpl(atom_service: AtomService):
        service_name = atom_service._base_info.get_name()
        server_impl_dir = f"{os.path.dirname(os.path.abspath(__file__))}/../../../db/atomic_service/{service_name}/sync_client_impl/"

        Util.compileCmakeProject(
            server_impl_dir,
            service_name + GrpcMethodUtil.grpc_service_sync_client_impl_suffix,
            file_type="cpp",
        )

    # def set_service_method_util(self, service: AtomService):
    #     self.__service_name = service._base_info.get_name()
    #     self.__operating_system = service._operating_systems
    #     self._service_methods = service._service_methods
    #     self._messages = service._messages
    #     self._generate_info()

    # def _check_situation(self) -> bool:
    #     if (
    #         self.__service_name == None
    #         or self.__operating_system == None
    #         or self._service_methods == None
    #         or self._messages == None
    #     ):
    #         return False
    #     return True

    # @staticmethod
    # def initial_info(atom_service: AtomService):
    #     pass

    # def _generate_info(self):
    #     self.__service_name_service = self.__service_name + "_Service"
    #     self.__service_name_package = self.__service_name + "_Package"
    #     self.__service_name_interface = self.__service_name + "_Interface"
