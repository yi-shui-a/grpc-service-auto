class BaseInfo:
    def __init__(self):
        self.__name = ""
        self.__chinese_name = ""
        self.__description = ""
        self.__version = ""
        self.__build_time = ""
        self.__priority_level = ""
        self.__license = ""
        self.__service_path = ""

    def getName(self):
        return self.__name

    def setName(self, name):
        self.__name = name

    def getChineseName(self):
        return self.__chinese_name

    def setChineseName(self, chinese_name):
        self.__chinese_name = chinese_name

    def getDescription(self):
        return self.__description

    def setDescription(self, description):
        self.__description = description

    def getVersion(self):
        return self.__version

    def setVersion(self, version):
        self.__version = version

    def getBuildTime(self):
        return self.__build_time

    def setBuildTime(self, build_time):
        self.__build_time = build_time

    def getPriorityLevel(self):
        return self.__priority_level

    def setPriorityLevel(self, priority_level):
        self.__priority_level = priority_level

    def getLicense(self):
        return self.__license

    def setLicense(self, license):
        self.__license = license

    def getServicePath(self):
        return self.__service_path

    def setServicePath(self, service_path):
        self.__service_path = service_path

    def set_info(self, info):
        self.__name = info.get("name", "")
        self.__chinese_name = info.get("chinese_name", "")
        self.__description = info.get("description", "")
        self.__version = info.get("version", "")
        self.__build_time = info.get("build_time", "")
        self.__priority_level = info.get("priority_level", -999)
        self.__license = info.get("license", "")
        self.__service_path = info.get("service_path", "")

    def set_all_info(self, name: str, chinese_name: str, description: str, version: str, build_time: str,
                     priority_level: int, license: str, service_path: str):
        self.__name = name
        self.__chinese_name = chinese_name
        self.__description = description
        self.__version = version
        self.__build_time = build_time
        self.__priorty_level = priority_level
        self.__license = license
        self.__service_path = service_path

    def to_dict(self):
        res_dict = dict()
        res_dict["name"] = self.__name
        res_dict["chinese_name"] = self.__chinese_name
        res_dict["description"] = self.__description
        res_dict["version"] = self.__version
        res_dict["build_time"] = self.__build_time
        res_dict["priority_level"] = self.__priority_level
        res_dict["license"] = self.__license
        res_dict["service_path"] = self.__service_path
        return res_dict

    def __str__(self) -> str:
        return f"Name: {self.__name}, Description: {self.__description},ChineseName: {self.__chinese_name}, Version: {self.__version}, BuildTime: {self.__build_time}, Priorty_level:{self.__priority_level}, License:{self.__license}, ServicePath: {self.__service_path}"


if __name__ == "__main__":
    baseInfo = BaseInfo()
    baseInfo.set_all_info("AXService", "AXService", "AXService", "1.0.0", "2022-01-01", 1, "MIT", "servicePath")
    print(baseInfo)
