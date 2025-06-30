import sys
import os
from jinja2 import Template
import subprocess
import json

from .Util import Util
from ..entity import Server
from ..enums import FileEnum


class ServerUtil:

    async_server_suffix = "_async_server"
    sync_server_suffix = "_sync_server"

    def __init__(self, server):
        # self._server: Server = server
        pass

    def saveServerJson(self):
        """
        保存服务器信息的 JSON 文件。此函数标志着一个服务器的生成。

        此方法将服务器的相关信息序列化为 JSON 格式，并将其保存到指定的文件路径中。
        具体步骤包括：
        1. 构建服务器信息文件存储的目录路径。
        2. 确保该目录存在，如果不存在则创建。
        3. 构建完整的 JSON 文件路径。
        4. 将服务器对象转换为字典，并写入 JSON 文件。
        5. 成功保存后打印成功消息；若过程中发生异常，则捕获并打印错误信息。

        参数:
            server: Server

        返回:
            无
        """
        Util.saveFile(
            name_list=[self.get_name()],
            content=json.dumps(self.to_dict(), indent=4),
            type=FileEnum.SERVER_JSON,
        )

    @staticmethod
    def generateSyncServer(server: Server):
        """
        添加header和moniter
        """
        Util.generateHeaderHppAndCpp(
            f"{os.path.dirname(os.path.abspath(__file__))}/../../../db/server/{server.get_name()}/sync_server/"
        )
        ServerUtil.generateMonitor(server)

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
            file_type="cpp",
        )

    @staticmethod
    def get_name_list(server: Server):
        # 从 self._server._services 列表中取出每个 service 的 name 变量，并组成一个字符串
        service_names = [service["grpc_info"]["name"] for service in server._services]
        return " ".join(service_names)

    @staticmethod
    def generateMonitor(server: Server):
        # 定义模板
        hpp_template = Template(
            open(
                f"{os.path.dirname(os.path.abspath(__file__))}/../../templates/registry_comm_template/monitorHpp.j2"
            ).read()
        )

        cpp_template = Template(
            open(
                f"{os.path.dirname(os.path.abspath(__file__))}/../../templates/registry_comm_template/monitorCpp.j2"
            ).read()
        )

        hpp_str = hpp_template.render()

        cpp_str = cpp_template.render(
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

        # 将hpp_str写入框架内的hpp文件中，同名不同路径
        with open(
            f"{os.path.dirname(os.path.abspath(__file__))}/../../../db/server/{server.get_name()}/sync_server/monitor.h",
            "w",
        ) as file:
            file.write(hpp_str)
        print(
            f"{os.path.dirname(os.path.abspath(__file__))}/../../../db/server/{server.get_name()}/sync_server/monitor.h generated successfully!"
        )

        # 将cpp_str写入框架内的cpp文件中，同名不同路径
        with open(
            f"{os.path.dirname(os.path.abspath(__file__))}/../../../db/server/{server.get_name()}/sync_server/monitor.cpp",
            "w",
        ) as file:
            file.write(cpp_str)
        print(
            f"{os.path.dirname(os.path.abspath(__file__))}/../../../db/server/{server.get_name()}/sync_server/monitor.cpp generated successfully!"
        )

    @staticmethod
    def generateExecShell(server_name:str):
        shell_template = Template(
            open(
                f"{os.path.dirname(os.path.abspath(__file__))}/../../templates/monitor_deployment_template/exec_server_shell_template.j2"
            ).read()
        )
        res_str = shell_template.render(
        server_name=server_name,
        )
        # 确保目录存在
        os.makedirs(
            "/opt/",
            exist_ok=True,
        )

        # 将res_str写入框架内的cpp文件中，同名不同路径
        with open(os.path.join("/opt/",f"{server_name}.sh"), "w",) as file:
            file.write(res_str)
        print(f"SUCCESS: generated /opt/{server_name}.sh")