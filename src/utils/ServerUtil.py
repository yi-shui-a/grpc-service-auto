import sys
import os
from jinja2 import Template

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
            f"{os.path.dirname(os.path.abspath(__file__))}/../../server_src/{self._server.get_name()}_async.cpp",
            "w",
        ) as file:
            file.write(res_str)
        print(
            f"{os.path.dirname(os.path.abspath(__file__))}/../../server_src/{self._server.get_name()}_async.cpp generated successfully!"
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
            f"{os.path.dirname(os.path.abspath(__file__))}/../../server_src/{self._server.get_name()}_sync.cpp",
            "w",
        ) as file:
            file.write(res_str)
        print(
            f"{os.path.dirname(os.path.abspath(__file__))}/../../server_src/{self._server.get_name()}_sync.cpp generated successfully!"
        )

    def generateClient(self):
        pass
