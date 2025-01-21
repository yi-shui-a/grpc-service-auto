from typing import Dict


class ReturnCode:

    def __init__(self):
        self.__return_value: Dict[str, int] = dict()

    def set_info(self, info: Dict[str, int]):
        self.__return_value.update(info)

    def add_return_value(self, key, value):
        self.__return_value[key] = value

    def set_return_value(self, key, value):
        self.__return_value[key] = value

    def remove_return_value(self, key):
        if key in self.__return_value:
            del self.__return_value[key]

    def get_return_value(self, key):
        self.__return_value.get(key)

    def get_return_key(self, value):
        # 根据值查找键
        for k, v in self.__return_value.items():
            if v == value:
                return k
        return None

    def get_return_values(self):
        return self.__return_value

    def clear_return_values(self):
        self.__return_value.clear()

    def to_dict(self):
        return self.__return_value.copy()

    def __str__(self):
        return f"Return Code: {self.__return_value}"


if __name__ == "__main__":
    res = ReturnCode()
    d = {"sadasads": 2, "asfdaf": 3}
    res.set_info(d)

    print(res.to_dict())
