import json
import sys
import os

from .AXService import AXService
from .OperatingSystem import OperatingSystem
from .Message import Message
from .GrpcMethod import GrpcMethod


class AtomService(AXService):
    def __init__(self):
        super().__init__()

    def to_dict(self) -> dict:
        res_dict = dict()
        res_dict["basic_info"] = self._base_info.to_dict()
        res_dict["basic_info"]["owner"] = self._owner.to_dict()
        res_dict["basic_info"][
            "resource_requirement"
        ] = self._resource_requirement.to_dict()
        res_dict["basic_info"]["operating_system"] = []
        for item in self._operating_systems:
            res_dict["basic_info"]["operating_system"].append(item.to_dict())
        # res_dict['basic_info']['operating_system'] = self._operating_systems.to_dict()
        res_dict["return_code"] = self._return_code.to_dict()
        message_list = list()
        for message in self._messages:
            message_list.append(message.to_dict())
        res_dict["messages"] = message_list

        method_list = list()
        for method in self._service_methods:
            method_list.append(method.to_dict())
        res_dict["grpc_methods"] = method_list

        # print(json.dumps(res_dict))
        return res_dict

    def set_info(self, info):
        self._base_info.set_info(info["basic_info"])
        self._owner.set_info(info["basic_info"]["owner"])
        self._resource_requirement.set_info(info["basic_info"]["resource_requirement"])
        self._return_code.set_info(info["return_code"])
        # 创建operating_systems
        for item in info["basic_info"]["operating_system"]:
            system = OperatingSystem()
            system.set_info(item)
            self._operating_systems.append(system)

        # 创建messages
        for item in info["messages"]:
            msg = Message()
            msg.set_info(item)
            self.add_message(msg)
        # 创建_rpc_service_methods
        for item in info["grpc_methods"]:
            # method = GrpcMethod.GrpcMethod(return_code= self._return_code,messages=self._messages)
            method = GrpcMethod(return_code=self._return_code, messages=self._messages)
            method.set_info(item)
            # for msg in self._messages:
            #     if msg._name == item["requestMsg"]:
            #         method._requestMsg = msg
            #     elif msg._name == item["responseMsg"]:
            #         method._responseMsg = msg
            self.add_service_method(method)
