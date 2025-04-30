import sys
import os
from typing import List
from abc import abstractmethod

from .Message import Message
from .ReturnCode import ReturnCode
from .Capabilities import Capabilities


class ServiceMethod:
    def __init__(self, return_code=None, messages=None):
        self._name: str = ""
        self._description: str = ""
        self._capabilities: Capabilities = Capabilities()
        self._return_code: ReturnCode = return_code
        self._messages: List[Message] = messages
        self._requestMsg: Message = None
        self._responseMsg: Message = None

    def set_info(self, info):
        self._name = info.get("name", "")
        self._description = info.get("description", "")
        self._capabilities.set_info(info["capabilities"])
        for message in self._messages:
            if message._name == info["requestMsg"]:
                self._requestMsg = message
            if message._name == info["responseMsg"]:
                self._responseMsg = message

    def to_dict(self):
        res_dict = dict()
        res_dict["name"] = self._name
        res_dict["description"] = self._description

        if self._requestMsg is None:
            res_dict["requestMsg"] = ""
        else:
            res_dict["requestMsg"] = self._requestMsg.get_name()

        if self._responseMsg is None:
            res_dict["responseMsg"] = ""
        else:
            res_dict["responseMsg"] = self._responseMsg.get_name()
        # res_dict["requestMsg"] = self._requestMsg.get_name()
        # res_dict["responseMsg"] = self._responseMsg.get_name()
        res_dict["capabilities"] = self._capabilities.to_dict()
        return res_dict

    def __str__(self):
        return f"Request Message: {self._requestMsg}, Response Message: {self._responseMsg}, Capabilities: {self._capabilities}"
