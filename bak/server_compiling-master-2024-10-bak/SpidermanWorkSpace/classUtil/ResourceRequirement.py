class ResourceRequirement:
    def __init__(self):
        self.__cpu_architecure = ""
        self.__memory_size = ""
        self.__hard_disk = ""

    def set_info(self, info):
        self.__cpu_architecure = info["cpu_architecture"]
        self.__memory_size = info["memory_size"]
        self.__hard_disk = info["hard_disk"]

    def toString(self)-> str:
        return f"CPU Architecture: {self.__cpu_architecure}, \
                Memory Size: {self.__memory_size}, \
                Hard Disk: {self.__hard_disk}"