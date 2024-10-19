import ReturnCode


class ServiceMethod:
    def __init__(self, return_code=None,messages=None):
        self._name = ""
        self._description = ""
        self._return_code = return_code
        self._messages = messages

    def setReturnCode(self, return_code):
        self._return_code = return_code

    def set_info(self, info):
        self._name = info["name"]
        self._description = info["description"]

    def to_dict(self):
        pass