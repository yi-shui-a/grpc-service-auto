class Maintainer:
    def __init__(self):
        self.__name: str = ""
        self.__email: str = ""

    def get_name(self):
        return self.__name

    def get_email(self):
        return self.__email

    def set_name(self, name):
        self.__name = name

    def set_email(self, email):
        self.__email = email

    def set_info(self, info: dict):
        self.__name = info.get("name", "")
        self.__email = info.get("email", "")

    def set_all_info(self, name: str, email: str):
        self.__name = name
        self.__email = email

    def to_dict(self):
        res_dict = dict()
        res_dict["name"] = self.__name
        res_dict["email"] = self.__email
        return res_dict

    def __str__(self) -> str:
        return f"Mainter Name: {self.__name}, Mainter Email: {self.__email}"
