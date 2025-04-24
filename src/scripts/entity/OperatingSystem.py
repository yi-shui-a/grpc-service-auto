class OperatingSystem:
    def __init__(self):
        self.__os_name: str = ""
        self.__os_version: dict = dict()

    def get_os_name(self):
        return self.__os_name

    def get_os_version(self):
        return self.__os_version

    def set_os_name(self, os_name):
        self.__os_name = os_name

    def set_os_version(self, os_version):
        self.__os_version = os_version

    def set_info(self, info):
        self.__os_name = info.get("os_name", "")
        self.__os_version = info.get("os_version", {})

    def set_all_info(self, name, version):
        self.__os_name = name
        self.__os_version = version

    def to_dict(self):
        res_dict = dict()
        res_dict["os_name"] = self.__os_name
        res_dict["os_version"] = self.__os_version
        return res_dict

    def __str__(self) -> str:
        return f"Operating System Name: {self.__os_name}, Operating System Version: {self.__os_version}"
