class BaseInfo:
    def __init__(self):
        self.__name = ""
        self.__chinese_name = ""
        self.__description = ""
        self.__version = ""
        self.__build_time = ""
        self.__priorty_level = ""
        self.__license = ""
        self.__servicePath = ""
    
    def set_info(self, info):
        self.__name = info["name"]
        self.__chinese_name = info["chinese_name"]
        self.__description = info["description"]
        self.__version = info["version"]
        self.__build_time = info["build_time"]
        self.__priorty_level = info["priorty_level"]
        self.__license = info["license"]
        self.__servicePath = info["servicePath"]

    def toString(self) -> str:
        return f"Name: {self.__name}, Description: {self.__description},ChineseName: {self.__chinese_name}, \
                Version: {self.__version}, BuildTime: {self.__build_time}, Priorty_level:{self.__priorty_level}, \
                License:{self.__license}, ServicePath: {self.__servicePath}"

    def set_all_info(self, name:str, chinese_name:str,description:str,version:str,build_time:str,priorty_level:int,license:str,servicePath:str):
        self.name = name
        self.chinese__name = chinese_name
        self.description = description
        self.version = version
        self.build_time = build_time
        self.priorty_level = priorty_level
        self.license = license
        self.servicePath = servicePath
    
if __name__ == "__main__":
    baseInfo = BaseInfo()
    print(baseInfo.description)
    baseInfo.set_info("AXService", "AXService", "AXService", "1.0.0", "2022-01-01", 1, "MIT", "servicePath")
    print(baseInfo.description)