import sys
import os
from jinja2 import Template
import subprocess

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir))
from Client import Client
from util.Util import Util


class ClientUtil:

    async_client_suffix = "_async_client"
    sync_client_suffix = "_sync_client"

    def __init__(self, client):
        pass

    @staticmethod
    def generateSyncServer(client: Client):
        # TODO: 通过json和client自动生成client
        pass
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
    def generateSyncClientCMakeLists(client: Client):
        client_template = Template(
            open(
                f"{os.path.dirname(os.path.abspath(__file__))}/../../templates/sync_server_client_process_template/sync_client_compile_cmake_template.j2"
            ).read()
        )
        res_str = client_template.render(
            project_name=client.get_name() + ClientUtil.sync_client_suffix,
            services=client._services,
            idl_list=client._dds_topic,
        )

        # 确保目录存在
        os.makedirs(
            f"{os.path.dirname(os.path.abspath(__file__))}/../../../db/client/{client.get_name()}/sync_client/",
            exist_ok=True,
        )

        # 将res_str写入框架内的cpp文件中，同名不同路径
        with open(
            f"{os.path.dirname(os.path.abspath(__file__))}/../../../db/client/{client.get_name()}/sync_client/CMakeLists.txt",
            "w",
        ) as file:
            file.write(res_str)
        print(
            f"{os.path.dirname(os.path.abspath(__file__))}/../../../db/client/{client.get_name()}/sync_client/CMakeLists.txt generated successfully!"
        )

    @staticmethod
    def compileSyncClient(client: Client):
        client_dir = f"{os.path.dirname(os.path.abspath(__file__))}/../../../db/client/{client.get_name()}/sync_client/"

        Util.compileCmakeProject(
            client_dir,
            client.get_name() + ClientUtil.sync_client_suffix,
            file_type="cpp",
        )

    # def _get_name_list(self):
    #     # 从 self._client._services 列表中取出每个 service 的 name 变量，并组成一个字符串
    #     service_names = [
    #         service["grpc_info"]["name"] for service in self._client._services
    #     ]
    #     return " ".join(service_names)

    # def generateAsyncClient(self):
    #     pass

    # def generateSyncClient(self):
    #     pass

    # def compileAsyncClient(self):
    #     pass

    # def compileSyncClient(self):
    #     filename = self._client._sync_client_name.split(".")[0]
    #     topic_str = " ".join(self._client._dds_topic)

    #     # 定义make命令及其参数
    #     make_command = [
    #         "make",
    #         "-C",
    #         f"{os.path.dirname(os.path.abspath(__file__))}/make/",
    #         "-f",
    #         "DDS_client_make",
    #         f"SERVICE={self._get_name_list()}",
    #         f"TOPIC={topic_str}",
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

    #     topic_str = " ".join(self._client._dds_topic)
    #     # 定义make命令及其参数
    #     make_command = [
    #         "make",
    #         "-C",
    #         f"{os.path.dirname(os.path.abspath(__file__))}/make/",
    #         "-f",
    #         "DDS_client_make",
    #         f"SERVICE={self._get_name_list()}",
    #         f"TOPIC={topic_str}",
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
