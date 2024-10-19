from .return_code import ReturnCode

class ServiceMethod:
    def __init__(self, name: str, chinese_name: str, description: str, return_code: ReturnCode):
        self.name = name
        self.chinese_name = chinese_name
        self.description = description
        self.return_code = return_code