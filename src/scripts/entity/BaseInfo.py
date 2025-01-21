class BaseInfo:
    def __init__(self):
        self.__name: str = ""
        self.__chinese_name: str = ""
        self.__description: str = ""
        self.__version: str = ""
        self.__build_time: str = ""
        self.__priority_level: str = ""
        self.__license: str = ""
        self.__service_path: str = ""

    def get_name(self):
        return self.__name

    def set_name(self, name):
        self.__name = name

    def get_chinese_name(self):
        return self.__chinese_name

    def set_chinese_name(self, chinese_name):
        self.__chinese_name = chinese_name

    def get_description(self):
        return self.__description

    def set_description(self, description):
        self.__description = description

    def get_version(self):
        return self.__version

    def set_version(self, version):
        self.__version = version

    def get_build_time(self):
        return self.__build_time

    def setB_build_time(self, build_time):
        self.__build_time = build_time

    def get_priority_level(self):
        return self.__priority_level

    def set_priority_level(self, priority_level):
        self.__priority_level = priority_level

    def get_license(self):
        return self.__license

    def set_license(self, license):
        self.__license = license

    def get_service_path(self):
        return self.__service_path

    def set_service_path(self, service_path):
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

    def set_all_info(
        self,
        name: str,
        chinese_name: str,
        description: str,
        version: str,
        build_time: str,
        priority_level: int,
        license: str,
        service_path: str,
    ):
        self.__name = name
        self.__chinese_name = chinese_name
        self.__description = description
        self.__version = version
        self.__build_time = build_time
        self.__priority_level = priority_level
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
    baseInfo.set_all_info(
        "AXService",
        "AXService",
        "AXService",
        "1.0.0",
        "2022-01-01",
        1,
        "MIT",
        "servicePath",
    )
    print(baseInfo)
