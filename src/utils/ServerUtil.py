import sys
import os
from jinja2 import Template
import subprocess

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
import Server


class ServerUtil:
    def __init__(self, server):
        self._server: Server.Server = server

    # def generateServerJson(self):
    #     pass

    def generateAsyncServer(self):
        # 定义模板
        proto_template = Template(
            open(
                f"{os.path.dirname(os.path.abspath(__file__))}/../../Jinja2/asyn_server_template.j2"
            ).read()
        )

        res_str = proto_template.render(
            services=self._server._services,
            name=self._server.get_name(),
            ip=self._server.get_ip(),
            port=self._server.get_port(),
            username=self._server.get_username(),
            password=self._server.get_password(),
            broadcast_address=self._server.get_broadcast_address(),
            broadcast_port=self._server.get_broadcast_port(),
        )

        # 将res_str写入框架内的cpp文件中，同名不同路径
        with open(
            f"{os.path.dirname(os.path.abspath(__file__))}/../../server_src/{self._server._async_server_name}.cpp",
            "w",
        ) as file:
            file.write(res_str)
        print(
            f"{os.path.dirname(os.path.abspath(__file__))}/../../server_src/{self._server._async_server_name}.cpp generated successfully!"
        )

    def generateSyncServer(self):
        # 定义模板
        proto_template = Template(
            open(
                f"{os.path.dirname(os.path.abspath(__file__))}/../../Jinja2/sync_server_template.j2"
            ).read()
        )

        res_str = proto_template.render(
            services=self._server._services,
            name=self._server.get_name(),
            ip=self._server.get_ip(),
            port=self._server.get_port(),
            username=self._server.get_username(),
            password=self._server.get_password(),
            broadcast_address=self._server.get_broadcast_address(),
            broadcast_port=self._server.get_broadcast_port(),
        )

        # 将res_str写入框架内的cpp文件中，同名不同路径
        with open(
            f"{os.path.dirname(os.path.abspath(__file__))}/../../server_src/{self._server._sync_server_name}.cpp",
            "w",
        ) as file:
            file.write(res_str)
        print(
            f"{os.path.dirname(os.path.abspath(__file__))}/../../server_src/{self._server._sync_server_name}.cpp generated successfully!"
        )

    def generateAsyncClient(self):
        pass

    def generateSyncClient(self):
        pass

    def _get_name_list(self):
        # 从 self._server._services 列表中取出每个 service 的 name 变量，并组成一个字符串
        service_names = [
            service["grpc_info"]["name"] for service in self._server._services
        ]
        return " ".join(service_names)

    def compileAsyncServer(self):
        # 定义make命令及其参数
        make_command = [
            "make",
            "-C",
            f"{os.path.dirname(os.path.abspath(__file__))}/make/",
            "-f",
            "test2_make",
            f"SERVICE={self._get_name_list()}",
            f"SERVER={self._server._async_server_name}",
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

    def compileSyncServer(self):
        """
        make -f test2_make SERVICE="atomic_service_mbsb atomic_service_sf" SERVER="client_sync_demo"
        """
        # 定义make命令及其参数
        make_command = [
            "make",
            "-C",
            f"{os.path.dirname(os.path.abspath(__file__))}/make/",
            "-f",
            "test2_make",
            f"SERVICE={self._get_name_list()}",
            f"SERVER={self._server._sync_server_name}",
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

    def compileAsyncClient(self):
        pass

    def compileSyncClient(self):
        pass

    def compileDemo(self, filename):
        # 定义make命令及其参数
        make_command = [
            "make",
            "-C",
            f"{os.path.dirname(os.path.abspath(__file__))}/make/",
            "-f",
            "test2_make",
            f"SERVICE={self._get_name_list()}",
            f"SERVER={filename}",
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
