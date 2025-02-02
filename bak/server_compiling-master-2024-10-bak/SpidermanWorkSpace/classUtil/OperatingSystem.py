class OperatingSystem:
    def __init__(self):
        self.__os_name = ""
        self.__os_version = ""
        # self.__os_architecture = ""
    
    def set_info(self, info):
        self.__os_name = info["os_name"]
        self.__os_version = info["os_version"]
        # self.__os_architecture = info["os_architecture"]
    
    def toString(self)->str:
        return f"Operating System Name: {self.__os_name}, Operating System Version: {self.__os_version}"