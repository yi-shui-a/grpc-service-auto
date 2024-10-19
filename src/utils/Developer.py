class Developer:
    def __init__(self):
        self.__name = ""
        self.__email = ""

    def get_name(self):
        return self.__name

    def get_email(self):
        return self.__email

    def set_name(self, name):
        self.__name = name

    def set_email(self, email):
        self.__email = email

    def set_info(self, info):
        self.__name = info["name"]
        self.__email = info["email"]

    def set_all_info(self, name, email):
        self.__name = name
        self.__email = email

    def to_dict(self):
        res_dict = dict()
        res_dict["name"] = self.__name
        res_dict["email"] = self.__email
        return res_dict

    def __str__(self) -> str:
        return f"Developer Name: {self.__name}, Developer Email: {self.__email}"
