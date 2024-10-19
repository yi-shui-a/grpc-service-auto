from typing import Dict

class ReturnCode:
    def __init__(self):
        self.returnValue: Dict[str, int] = {}

    def addReturnValue(self, key: str, value: int) -> bool:
        if key in self.returnValue:
            return False
        self.returnValue[key] = value
        return True

    def setReturnValue(self, key: str, value: int) -> bool:
        self.returnValue[key] = value
        return True

    def removeReturnValue(self, key: str) -> bool:
        if key not in self.returnValue:
            return False
        del self.returnValue[key]
        return True

    def getReturnValue(self, key: str) -> int:
        return self.returnValue.get(key, -1)

    def getReturnKey(self, value: int) -> str:
        for k, v in self.returnValue.items():
            if v == value:
                return k
        return ""

    def __str__(self):
        return str(self.returnValue)