import sys
import os
from jinja2 import Template
import subprocess

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from Server import Server
from util.Util import Util


class ServerUtil:

    async_server_suffix = "_async_server"
    sync_server_suffix = "_sync_server"

    def __init__(self, server):
        # self._server: Server = server
        pass

    @staticmethod
    def generateSyncServer(server: Server):
        # 定义模板
        proto_template = Template(
            open(
                f"{os.path.dirname(os.path.abspath(__file__))}/../../templates/sync_server_client_process_template/sync_server_template.j2"
            ).read()
        )

        res_str = proto_template.render(
            services=server._services,
            name=server.get_name(),
            ip=server.get_ip(),
            port=server.get_port(),
            username=server.get_username(),
            password=server.get_password(),
            broadcast_address=server.get_broadcast_address(),
            broadcast_port=server.get_broadcast_port(),
        )

        # 确保目录存在
        os.makedirs(
            f"{os.path.dirname(os.path.abspath(__file__))}/../../../db/server/{server.get_name()}/sync_server/",
            exist_ok=True,
        )

        # 将res_str写入框架内的cpp文件中，同名不同路径
        with open(
            f"{os.path.dirname(os.path.abspath(__file__))}/../../../db/server/{server.get_name()}/sync_server/{server.get_name() + ServerUtil.sync_server_suffix}.cpp",
            "w",
        ) as file:
            file.write(res_str)
        print(
            f"{os.path.dirname(os.path.abspath(__file__))}/../../../db/server/{server.get_name()}/sync_server/{server.get_name() + ServerUtil.sync_server_suffix}.cpp generated successfully!"
        )

    @staticmethod
    def generateSyncServerCMakeLists(server: Server):
        server_template = Template(
            open(
                f"{os.path.dirname(os.path.abspath(__file__))}/../../templates/sync_server_client_process_template/sync_server_compile_cmake_template.j2"
            ).read()
        )
        res_str = server_template.render(
            project_name=server.get_name() + ServerUtil.sync_server_suffix,
            services=server._services,
        )

        # 确保目录存在
        os.makedirs(
            f"{os.path.dirname(os.path.abspath(__file__))}/../../../db/server/{server.get_name()}/sync_server/",
            exist_ok=True,
        )

        # 将res_str写入框架内的cpp文件中，同名不同路径
        with open(
            f"{os.path.dirname(os.path.abspath(__file__))}/../../../db/server/{server.get_name()}/sync_server/CMakeLists.txt",
            "w",
        ) as file:
            file.write(res_str)
        print(
            f"{os.path.dirname(os.path.abspath(__file__))}/../../../db/server/{server.get_name()}/sync_server/CMakeLists.txt generated successfully!"
        )

    @staticmethod
    def compileSyncServer(server: Server):
        server_dir = f"{os.path.dirname(os.path.abspath(__file__))}/../../../db/server/{server.get_name()}/sync_server/"

        Util.compileCmakeProject(
            server_dir,
            server.get_name() + ServerUtil.sync_server_suffix,
            cpp_file_type="cpp",
        )

    @staticmethod
    def get_name_list(server: Server):
        # 从 self._server._services 列表中取出每个 service 的 name 变量，并组成一个字符串
        service_names = [service["grpc_info"]["name"] for service in server._services]
        return " ".join(service_names)

    # def compileSyncServer(self):
    #     """
    #     make -f test2_make SERVICE="atomic_service_mbsb atomic_service_sf" SERVER="client_sync_demo"
    #     """
    #     # 定义make命令及其参数
    #     make_command = [
    #         "make",
    #         "-C",
    #         f"{os.path.dirname(os.path.abspath(__file__))}/make/",
    #         "-f",
    #         "test2_make",
    #         f"SERVICE={self._get_name_list()}",
    #         f"SERVER={self._server._sync_server_name}",
    #     ]

    #     try:
    #         # 调用make命令，并等待其完成
    #         result = subprocess.run(
    #             make_command,
    #             check=True,
    #             stdout=subprocess.PIPE,
    #             stderr=subprocess.PIPE,
    #             text=True,
    #         )

    #         # 如果make命令成功执行，则打印其输出
    #         if result.stdout:
    #             print("Make Output:\n", result.stdout)

    #     except subprocess.CalledProcessError as e:
    #         # 如果make命令失败，则捕获异常并打印错误信息
    #         print("Make failed with error:", e)
    #         print("Error Output:\n", e.stderr)

    # def generateAsyncServer(self):
    #     # 定义模板
    #     proto_template = Template(
    #         open(
    #             f"{os.path.dirname(os.path.abspath(__file__))}/../../src/templates/asyn_server_template.j2"
    #         ).read()
    #     )

    #     res_str = proto_template.render(
    #         services=self._server._services,
    #         name=self._server.get_name(),
    #         ip=self._server.get_ip(),
    #         port=self._server.get_port(),
    #         username=self._server.get_username(),
    #         password=self._server.get_password(),
    #         broadcast_address=self._server.get_broadcast_address(),
    #         broadcast_port=self._server.get_broadcast_port(),
    #     )

    #     # 确保目录存在
    #     os.makedirs(
    #         f"{os.path.dirname(os.path.abspath(__file__))}/../../server_src/",
    #         exist_ok=True,
    #     )

    #     # 将res_str写入框架内的cpp文件中，同名不同路径
    #     with open(
    #         f"{os.path.dirname(os.path.abspath(__file__))}/../../server_src/{self._server._async_server_name}.cpp",
    #         "w",
    #     ) as file:
    #         file.write(res_str)
    #     print(
    #         f"{os.path.dirname(os.path.abspath(__file__))}/../../server_src/{self._server._async_server_name}.cpp generated successfully!"
    #     )

    # def compileAsyncServer(self):
    #     # 定义make命令及其参数
    #     make_command = [
    #         "make",
    #         "-C",
    #         f"{os.path.dirname(os.path.abspath(__file__))}/make/",
    #         "-f",
    #         "test2_make",
    #         f"SERVICE={self._get_name_list()}",
    #         f"SERVER={self._server._async_server_name}",
    #     ]
    #     try:
    #         # 调用make命令，并等待其完成
    #         result = subprocess.run(
    #             make_command,
    #             check=True,
    #             stdout=subprocess.PIPE,
    #             stderr=subprocess.PIPE,
    #             text=True,
    #         )

    #         # 如果make命令成功执行，则打印其输出
    #         if result.stdout:
    #             print("Make Output:\n", result.stdout)

    #     except subprocess.CalledProcessError as e:
    #         # 如果make命令失败，则捕获异常并打印错误信息
    #         print("Make failed with error:", e)
    #         print("Error Output:\n", e.stderr)

    # def compileServerDemo(self, filename):
    #     # 定义make命令及其参数
    #     make_command = [
    #         "make",
    #         "-C",
    #         f"{os.path.dirname(os.path.abspath(__file__))}/make/",
    #         "-f",
    #         "test2_make",
    #         f"SERVICE={self._get_name_list()}",
    #         f"SERVER={filename}",
    #     ]
    #     try:
    #         # 调用make命令，并等待其完成
    #         result = subprocess.run(
    #             make_command,
    #             check=True,
    #             stdout=subprocess.PIPE,
    #             stderr=subprocess.PIPE,
    #             text=True,
    #         )

    #         # 如果make命令成功执行，则打印其输出
    #         if result.stdout:
    #             print("Make Output:\n", result.stdout)

    #     except subprocess.CalledProcessError as e:
    #         # 如果make命令失败，则捕获异常并打印错误信息
    #         print("Make failed with error:", e)
    #         print("Error Output:\n", e.stderr)

    # def compileDemo(self, filename: str):
    #     filename = filename.split(".")[0]
    #     # 定义make命令及其参数
    #     make_command = [
    #         "make",
    #         "-C",
    #         f"{os.path.dirname(os.path.abspath(__file__))}/make/",
    #         "-f",
    #         "test2_make",
    #         f"SERVICE={self._get_name_list()}",
    #         f"SERVER={filename}",
    #     ]
    #     try:
    #         # 调用make命令，并等待其完成
    #         result = subprocess.run(
    #             make_command,
    #             check=True,
    #             stdout=subprocess.PIPE,
    #             stderr=subprocess.PIPE,
    #             text=True,
    #         )

    #         # 如果make命令成功执行，则打印其输出
    #         if result.stdout:
    #             print("Make Output:\n", result.stdout)

    #     except subprocess.CalledProcessError as e:
    #         # 如果make命令失败，则捕获异常并打印错误信息
    #         print("Make failed with error:", e)
    #         print("Error Output:\n", e.stderr)
