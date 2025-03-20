import sys
import os
from typing import List
from abc import abstractmethod

from .Message import Message
from .ReturnCode import ReturnCode


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
