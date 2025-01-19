class ReturnCode():
    __return_value = []

    def __init__(self):
        pass

    @classmethod
    def set_info(self, info):
        for k, v in info.items():
            self.addReturnValue(k, v)

    @classmethod
    def addReturnValue(self, key, value):
        ReturnCode.__return_value.append((key, value))

    @classmethod
    def setReturnValue(self, key, value):
        for i, (k, v) in enumerate(ReturnCode.__return_value):
            if k == key:
                ReturnCode.__return_value[i] = (key, value)

    @classmethod
    def removeReturnValue(self, key, value):
        ReturnCode.__return_value.remove(key)

    @classmethod
    def getReturnValue(self, key):
        for k, v in ReturnCode.__return_value:
            if k == key:
                return v
        return None

    @classmethod
    def getReturnKey(self, value):
        for i, (k, v) in enumerate(ReturnCode.__return_value):
            if v == value:
                return k
        return None

    @classmethod
    def getReturnValues(self):
        return ReturnCode.__return_value

    @classmethod
    def clearReturnValues(self):
        ReturnCode.__return_value = []

    @classmethod
    def to_dict(self):
        res_dict = dict()
        for i, (k, v) in enumerate(ReturnCode.__return_value):
            res_dict[str(k)] = v
        return res_dict

    def __str__(self):
        return f"Return Code: {ReturnCode.__return_value}"


if __name__ == '__main__':
    res = ReturnCode()
    d = {"sadasads": 2, "asfdaf": 3}
    res.set_info(d)

    print(res.to_dict())
