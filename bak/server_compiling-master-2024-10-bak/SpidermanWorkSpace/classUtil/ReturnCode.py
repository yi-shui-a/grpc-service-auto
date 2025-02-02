class ReturnCode:
    def __init__(self):
        self._return_value = []

    def addReturnValue(self, key, value):
        self._return_value.append((key, value))
    def setReturnValue(self, key, value):
        for i, (k, v) in enumerate(self._return_value):
            if k == key:
                self._return_value[i] = (key, value)

    def removeReturnValue(self, key, value):
        self._return_value.remove(key)
    def getReturnValue(self, key):
        for k, v in self._return_value:
            if k == key:
                return v
        return None
    def getReturnKey(self, value):
        for i, (k, v) in enumerate(self._return_value):
            if v == value:
                return k
        return None

    def getReturnValues(self):
        return self._return_value
    def clearReturnValues(self):
        self._return_value = []


    def toString(self):
        return f"Return Code: {self._return_value}"
        
