import Mainter
import Developer

class Owner:
    def __init__(self):
        self.__mainter = Mainter.Mainter()
        self.__developer = Developer.Developer()
    def set_info(self, info):
        self.__mainter.set_info(info["mainter"])
        self.__developer.set_info(info["developer"])

    def toString(self) -> str:
        return f"Mainter: {self.__mainter.toString()}, \
                Developer: {self.__developer.toString()}"
