import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from entity.Message import Message
from entity.Capabilities import Capabilities
from ServiceMethod import ServiceMethod


class GrpcMethod(ServiceMethod):
    def __init__(self, return_code=None, messages=None):
        super().__init__(return_code, messages)
        self._requestMsg: Message = Message()
        self._responseMsg: Message = Message()
        self._capabilities: Capabilities = Capabilities()

    def set_info(self, info):
        super().set_info(info)
        self._capabilities.set_info(info["capabilities"])
        for message in self._messages:
            if message._name == info["requestMsg"]:
                self._requestMsg = message
            elif message._name == info["responseMsg"]:
                self._responseMsg = message

    def to_dict(self):
        res_dict = dict()
        res_dict["name"] = self._name
        res_dict["description"] = self._description
        res_dict["requestMsg"] = self._requestMsg.get_name()
        res_dict["responseMsg"] = self._responseMsg.get_name()
        res_dict["capabilities"] = self._capabilities.to_dict()
        return res_dict

    def __str__(self):
        return f"Request Message: {self._requestMsg}, Response Message: {self._responseMsg}, Capabilities: {self._capabilities}"
