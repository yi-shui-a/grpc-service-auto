class Developer:
    def __init__(self):
        self.__name = ""
        self.__email = ""
    def set_info(self, info):
        self.__name = info["name"]
        self.__email = info["email"]

    def toString(self)->str:
        return f"Developer Name: {self.__name}, Developer Email: {self.__email}"
