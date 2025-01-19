import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
import Maintainer
import Developer


class Owner:
    def __init__(self):
        self.__maintainer = Maintainer.Maintainer()
        self.__developer = Developer.Developer()

    def get_maintainer(self):
        return self.__maintainer

    def get_developer(self):
        return self.__developer

    def set_maintainer(self, maintainer):
        self.__maintainer = maintainer

    def set_developer(self, developer):
        self.__developer = developer

    def set_info(self, info):
        self.__maintainer.set_info(info["maintainer"])
        self.__developer.set_info(info["developer"])

    def set_all_info(self, maintainer, developer):
        self.__maintainer = (maintainer, developer)
        self.__developer = (maintainer, developer)

    def to_dict(self):
        res_dict = dict()
        res_dict['maintainer'] = self.__maintainer.to_dict()
        res_dict['developer'] = self.__developer.to_dict()
        return res_dict

    def __str__(self) -> str:
        return f"Mainter: {self.__maintainer}, Developer: {self.__developer}"
