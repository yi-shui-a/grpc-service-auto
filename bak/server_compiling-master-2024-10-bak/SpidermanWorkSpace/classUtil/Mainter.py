class Mainter:
    def __init__(self):
        self.__name = ""
        self.__email = ""
    
    def set_info(self, info):
        self.__name = info["name"]
        self.__email = info["email"]

    def toString(self)->str:
        return f"Mainter Name: {self.__name}, Mainter Email: {self.__email}"
