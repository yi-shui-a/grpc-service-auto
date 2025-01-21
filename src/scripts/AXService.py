from typing import List
from abc import abstractmethod
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from entity.BaseInfo import BaseInfo
from entity.Owner import Owner
from entity.ResourceRequirement import ResourceRequirement
from entity.OperatingSystem import OperatingSystem
from entity.Message import Message
from entity.ReturnCode import ReturnCode
from GrpcMethod import GrpcMethod
from ServiceMethod import ServiceMethod


class AXService:
    def __init__(self):
        self._base_info: BaseInfo = BaseInfo()  # private
        self._owner: Owner = Owner()
        self._resource_requirement: ResourceRequirement = ResourceRequirement()
        self._operating_systems: List[OperatingSystem] = []
        self._return_code: ReturnCode = ReturnCode()
        self._messages: List[Message] = []  # public
        self._service_methods: List[ServiceMethod] = []  # public

    def add_message(self, message):
        self._messages.append(message)

    def add_service_method(self, service_method):
        self._service_methods.append(service_method)

    @abstractmethod
    def to_dict(self) -> dict:
        pass

    @abstractmethod
    def set_info(self, info):
        pass

    def __str__(self):
        print("BaseInfo: {}".format(self._base_info))
        print("Owner: {}".format(self._owner))
        print("Resource_Requirement: {}".format(self._resource_requirement))
        print("Operating_System: {}".format(self._operating_systems))


# eg: test
if __name__ == "__main__":
    axservice = AXService()
    info = {
        "baseinfo": {
            "name": "AXService",
            "chinese_name": "AXService",
            "description": "AXService",
            "version": "1.0.0",
            "build_time": "2022-01-01",
            "priorty_level": 1,
            "license": "MIT",
            "servicePath": "servicePath",
        },
        "owner": {
            "mainter": {"name": "Mainter", "email": "mainter@example.com"},
            "developer": {"name": "Developer", "email": "developer@example.com"},
        },
        "resource_requirement": {
            "cpu_architecture": 1,
            "memory_size": 1,
            "hard_disk": 1,
        },
        "operating_system": {
            "os_name": "OSName",
            "os_version": "OSVersion",
            "os_architecture": "OSArchitecture",
        },
    }

    axservice.set_info(info)
    print(axservice())
