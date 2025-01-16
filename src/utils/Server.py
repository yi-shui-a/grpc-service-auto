import sys
import os
from typing import List
import json

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
import AtomService


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
        self._heartbeat_interal = 30

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
        self._services.append(service)

    def delete_service(self, service: str):
        try:
            self._services.remove(service)
        except ValueError as e:
            print(f"Error: {e}")
            print(f"Service '{service}' not found in the list.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def set_service(self, old_service: str, new_service: str):
        for service in self._services:
            if service == old_service:
                service = new_service
                break

    def set_file_name(self):
        self._async_server_name = f"{self._name}_async_server"
        self._sync_server_name = f"{self._name}_sync_server"
        self._async_client_name = f"{self._name}_async_client"
        self._sync_client_name = f"{self._name}_sync_client"

    # 使用用户输入数据加载Server
    def set_info_from_user(self, info):
        self._name = info["name"]
        self._ip = info["ip"]
        self._port = info["port"]
        self._username = info["username"]
        self._password = info["password"]
        self._broadcast_address = info["broadcast_address"]
        self._broadcast_port = info["broadcast_port"]
        self._heartbeat_interal = info["heartbeat_interal"]
        self.set_file_name()
        # 将原子服务的json作为一个service的dict变量，全部传入
        for service in info["services"]:
            with open(
                f"{os.path.dirname(os.path.abspath(__file__))}/../../atom_json/{service}.json",
                "r",
            ) as file:
                # data = json.loads(file.read())
                self.add_service(json.loads(file.read()))

    # 加载json_client
    def set_info(self, info):
        self._name = info["name"]
        self._ip = info["ip"]
        self._port = info["port"]
        self._username = info["username"]
        self._password = info["password"]
        self._broadcast_address = info["broadcast_address"]
        self._broadcast_port = info["broadcast_port"]
        self._heartbeat_interal = info["heartbeat_interal"]

        self._async_server_name = info["async_server_name"]
        self._sync_server_name = info["sync_server_name"]

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

    def saveServerJson(
        self, path=f"{os.path.dirname(os.path.abspath(__file__))}/../../json_server/"
    ):
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
