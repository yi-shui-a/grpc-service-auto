class Capabilities:
    def __init__(self):
        self.__read:bool = False
        self.__write:bool = False
        self.__delete:bool = False

    def get_read(self):
        return self.__read

    def get_write(self):
        return self.__write

    def get_delete(self):
        return self.__delete

    def set_read(self, read):
        self.__read = read

    def set_write(self, write):
        self.__write = write

    def set_delete(self, delete):
        self.__delete = delete

    def set_all_info(self,read:bool,write:bool,delete:bool):
        self.__read = read
        self.__write = write
        self.__delete = delete

    def set_info(self,capabilities:dict):
        self.__read = capabilities['read']
        self.__write = capabilities['write']
        self.__delete = capabilities['delete']

    def to_dict(self) -> dict:
        res_dict = dict()
        res_dict['read'] = self.__read
        res_dict['write'] = self.__write
        res_dict['delete'] = self.__delete
        return res_dict

    def __str__(self):
        return f'read: {self.__read}, write: {self.__write}, delete: {self.__delete}'
