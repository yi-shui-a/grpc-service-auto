import sys
import os


from .Maintainer import Maintainer
from .Developer import Developer


class Owner:
    def __init__(self):
        self.__maintainer: Maintainer = Maintainer()
        self.__developer: Developer = Developer()

    def get_maintainer(self):
        return self.__maintainer

    def get_developer(self):
        return self.__developer

    def set_maintainer(self, maintainer):
        self.__maintainer = maintainer

    def set_developer(self, developer):
        self.__developer = developer

    def set_info(self, info: dict):
        self.__maintainer.set_info(info.get("maintainer", {}))
        self.__developer.set_info(info.get("developer", {}))

    def set_all_info(self, maintainer: Maintainer, developer: Developer):
        self.__maintainer = maintainer
        self.__developer = developer

    def to_dict(self):
        res_dict = dict()
        res_dict["maintainer"] = self.__maintainer.to_dict()
        res_dict["developer"] = self.__developer.to_dict()
        return res_dict

    def __str__(self) -> str:
        return f"Mainter: {self.__maintainer}, Developer: {self.__developer}"
