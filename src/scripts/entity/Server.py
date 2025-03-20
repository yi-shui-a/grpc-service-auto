import sys
import os
from typing import List
import json

# sys.path.append(os.path.abspath(os.path.dirname(__file__)))
# from scripts.entity.AtomService import AtomService
# from util.Config import Config

from ..config import Config


class Server:
    def __init__(self):
        self._name: str = ""
        self._services: List[dict] = []
        self._ip: str = ""
        self._port: str = ""
        self._username: str = ""
        self._password: str = ""
        self._broadcast_address: str = ""
        self._broadcast_port: str = ""
        try:
            # 尝试从 Config 中获取 heartbeat_interval 属性
            self._heartbeat_interal = Config().heartbeat_interval
        except AttributeError:
            raise AttributeError(
                "heartbeat_interval attribute is missing from Config class"
            )

        self._async_server_name: str = ""
        self._sync_server_name: str = ""

    def get_name(self) -> str:
        return self._name

    def set_name(self, name: str) -> None:
        self._name = name

    def get_ip(self) -> str:
        return self._ip

    def set_ip(self, ip: str) -> None:
        self._ip = ip

    def get_port(self) -> str:
        return self._port

    def set_port(self, port: str) -> None:
        self._port = port

    def get_username(self) -> str:
        return self._username

    def set_username(self, username: str) -> None:
        self._username = username

    def get_password(self):
        return self._password

    def set_password(self, password: str) -> None:
        self._password = password

    def get_broadcast_address(self):
        return self._broadcast_address

    def set_broadcast_address(self, broadcast_address: str) -> None:
        self._broadcast_address = broadcast_address

    def get_broadcast_port(self):
        return self._broadcast_port

    def set_broadcast_port(self, broadcast_port: str) -> None:
        self._broadcast_port = broadcast_port

    def add_service(self, service: str):
        # 将一个service的数据以dict的形式传给server
        with open(
            f"{os.path.dirname(os.path.abspath(__file__))}/../../db/atomic_service/{service}/{service}.json",
            "r",
        ) as file:
            self._services.append(json.loads(file.read()))

    def delete_service(self, service: str):
        # 创建一个新的列表，用于存储不需要删除的元素
        new_services = []
        found = False
        # 遍历原列表中的每个元素
        for s in self._services:
            # 检查当前元素的 "basic_info" 中的 "name" 是否等于要删除的服务名称
            if s["basic_info"]["name"] == service:
                found = True
            else:
                # 如果不等于，则将该元素添加到新列表中
                new_services.append(s)
        # 如果找到了要删除的服务，则更新原列表
        if found:
            self._services = new_services
        else:
            # 如果未找到，则输出错误信息
            print(f"Service '{service}' not found in the list.")

    def set_service(self, old_service: str, new_service: str):
        self.delete_service(old_service)
        self.add_service(new_service)

    # 使用用户输入数据加载Server
    def set_info_from_user(self, info: dict):
        self._name = info.get("name", "")
        self._ip = info.get("ip", "")
        self._port = info.get("port", "")
        self._username = info.get("username", "")
        self._password = info.get("password", "")
        self._broadcast_address = info.get("broadcast_address", "")
        self._broadcast_port = info.get("broadcast_port", "")
        self._heartbeat_interal = info.get("heartbeat_interval", "")
        # 将原子服务的json作为一个service的dict变量，全部传入
        for service in info["services"]:
            self.add_service(service)

    # 加载json_client
    def set_info(self, info: dict):
        self._name = info.get("name", "")
        self._ip = info.get("ip", "")
        self._port = info.get("port", "")
        self._username = info.get("username", "")
        self._password = info.get("password", "")
        self._broadcast_address = info.get("broadcast_address", "")
        self._broadcast_port = info.get("broadcast_port", "")
        self._heartbeat_interal = info.get.get("heartbeat_interval", "")

        self._async_server_name = info.get("async_server_name", "")
        self._sync_server_name = info.get("sync_server_name", "")

        for service in info["services"]:
            self.add_service(service)

    def to_dict(self):
        res_dict = dict()
        res_dict["name"] = self._name
        res_dict["ip"] = self._ip
        res_dict["port"] = self._port
        res_dict["username"] = self._username
        res_dict["password"] = self._password
        res_dict["broadcast_address"] = self._broadcast_address
        res_dict["broadcast_port"] = self._broadcast_port
        res_dict["heartbeat_interal"] = self._heartbeat_interal

        res_dict["async_server_name"] = self._async_server_name
        res_dict["sync_server_name"] = self._sync_server_name

        res_dict["services"] = self._services
        return res_dict

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
            无

        返回:
            无
        """
        path = f"{os.path.dirname(os.path.abspath(__file__))}/../../db/server/{self.get_name()}/"
        try:
            # 确保目录存在
            os.makedirs(path, exist_ok=True)

            # 构建完整的文件路径
            file_path = os.path.join(path, self.get_name()) + ".json"

            # 打开文件并写入 JSON 数据
            with open(file_path, "w") as file:
                json.dump(self.to_dict(), file, indent=4)

            print(f"{file_path} saved successfully!")
        except Exception as e:
            print(f"Error saving JSON file: {e}")
