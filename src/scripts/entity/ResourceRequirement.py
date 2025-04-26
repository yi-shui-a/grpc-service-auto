class ResourceRequirement:
    def __init__(self):
        self.__cpu_architecture: str = ""
        self.__memory: int = 0
        self.__hard_disk: int = 0

    def get_cpu_architecture(self):
        return self.__cpu_architecture

    def get_memory_size(self):
        return self.__memory

    def get_hard_disk(self):
        return self.__hard_disk

    def set_cpu_architecture(self, architecture: str):
        self.__cpu_architecture = architecture

    def set_memory_size(self, memory: str):
        self.__memory = memory

    def set_hard_disk(self, hard_disk: str):
        self.__hard_disk = hard_disk

    def set_info(self, info: dict):
        self.__cpu_architecture = info.get("cpu_architecture", "")
        self.__memory = info.get("memory", "")
        self.__hard_disk = info.get("hard_disk", "")

    def set_all_info(self, cpu_architecture: str, memory_size: str, hard_disk: str):
        self.__cpu_architecture = cpu_architecture
        self.__memory = memory_size
        self.__hard_disk = hard_disk

    def to_dict(self):
        res_dict = dict()
        res_dict["cpu_architecture"] = self.__cpu_architecture
        res_dict["memory"] = self.__memory
        res_dict["hard_disk"] = self.__hard_disk
        return res_dict

    def __str__(self) -> str:
        return f"CPU Architecture: {self.__cpu_architecture}, Memory Size: {self.__memory}, Hard Disk: {self.__hard_disk}"
