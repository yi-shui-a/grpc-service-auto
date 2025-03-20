import sys
import os
from typing import List
import json

# sys.path.append(os.path.abspath(os.path.dirname(__file__)))


class Client:
    def __init__(self):
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

    def add_service(self, service: str):
        # 将一个service的数据以dict的形式传给server
        with open(
            f"{os.path.dirname(os.path.abspath(__file__))}/../../../db/atomic_service/{service}/{service}.json",
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

    def add_dds_topic(self, dds_topic: str):
        self._dds_topic.append(dds_topic)

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
        # TODO: 保存一个client所有的数据
        pass
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
