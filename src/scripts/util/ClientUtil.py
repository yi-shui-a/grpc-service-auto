import sys
import os
from jinja2 import Template
import subprocess

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir))
from Client import Client


class ClientUtil:
    def __init__(self, client):
        self._client: Client = client

    # def generateServerJson(self):
    #     pass

    def _get_name_list(self):
        # 从 self._client._services 列表中取出每个 service 的 name 变量，并组成一个字符串
        service_names = [
            service["grpc_info"]["name"] for service in self._client._services
        ]
        return " ".join(service_names)

    def generateAsyncClient(self):
        pass

    def generateSyncClient(self):
        pass

    def compileAsyncClient(self):
        pass

    def compileSyncClient(self):
        filename = self._client._sync_client_name.split(".")[0]
        topic_str = " ".join(self._client._dds_topic)

        # 定义make命令及其参数
        make_command = [
            "make",
            "-C",
            f"{os.path.dirname(os.path.abspath(__file__))}/make/",
            "-f",
            "DDS_client_make",
            f"SERVICE={self._get_name_list()}",
            f"TOPIC={topic_str}",
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

    def compileDemo(self, filename: str):
        filename = filename.split(".")[0]

        topic_str = " ".join(self._client._dds_topic)
        # 定义make命令及其参数
        make_command = [
            "make",
            "-C",
            f"{os.path.dirname(os.path.abspath(__file__))}/make/",
            "-f",
            "DDS_client_make",
            f"SERVICE={self._get_name_list()}",
            f"TOPIC={topic_str}",
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
