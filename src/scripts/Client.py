import sys
import os
from typing import List
import json

sys.path.append(os.path.abspath(os.path.dirname(__file__)))


class Client:
    def __init__(self, server):
        self._name: str = ""
        self._dds_topic: List[str] = []
        self._services: List[dict] = []

        self._async_client_name: str = ""
        self._sync_client_name: str = ""

    def set_file_name(self):
        self._async_client_name = f"{self._name}_async_client"
        self._sync_client_name = f"{self._name}_sync_client"

    def get_name(self) -> str:
        return self._name

    def set_name(self, name: str) -> None:
        self._name = name

    def add_dds_topic(self, dds_topic: str):
        self._dds_topic.append(dds_topic)

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

    def delete_dds_topic(self, topic: str):
        try:
            self._dds_topic.remove(topic)
        except ValueError as e:
            print(f"Error: {e}")
            print(f"Topic '{topic}' not found in the list.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def set_dds_topic(self, old_topic: str, new_topic: str):
        for index in range(0, len(self._dds_topic)):
            if self._dds_topic[index] == old_topic:
                self._dds_topic[index] = new_topic
                break

    def set_service(self, old_service: str, new_service: str):
        for index in range(0, len(self._services)):
            if self._services[index] == old_service:
                self._services[index] = new_service
                break

    # 使用用户输入数据加载Client
    def set_info_from_user(self, info):
        self._name = info["name"]
        self.set_info_from_user()
        # 将原子服务的json作为一个service的dict变量，全部传入
        for service in info["services"]:
            with open(
                f"{os.path.dirname(os.path.abspath(__file__))}/../../atom_json/{service}.json",
                "r",
            ) as file:
                # data = json.loads(file.read())
                self.add_service(json.loads(file.read()))

    # 加载client_json
    def set_info(self, info):
        self._name = info["name"]

        self._async_client_name = info["async_client_name"]
        self._sync_client_name = info["sync_client_name"]

        for service in info["services"]:
            self.add_service(service)

    def to_dict(self):
        res_dict = dict()
        res_dict["name"] = self._name

        res_dict["async_client_name"] = self._async_client_name
        res_dict["sync_client_name"] = self._sync_client_name

        res_dict["services"] = self._services
        return res_dict

    def saveClientJson(
        self, path=f"{os.path.dirname(os.path.abspath(__file__))}/../../json_client/"
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
