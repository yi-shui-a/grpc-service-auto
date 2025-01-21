import sys
import os
from typing import List
from abc import abstractmethod

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from entity.ReturnCode import ReturnCode
from entity.Message import Message


class ServiceMethod:
    def __init__(self, return_code=None, messages=None):
        self._name: str = ""
        self._description: str = ""
        self._return_code: ReturnCode = return_code
        self._messages: List[Message] = messages

    def setReturnCode(self, return_code):
        self._return_code = return_code

    def set_info(self, info):
        self._name = info["name"]
        self._description = info["description"]

    @abstractmethod
    def to_dict(self):
        pass
