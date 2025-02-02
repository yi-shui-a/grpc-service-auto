import ReturnCode


class ServiceMethod:
    def __init__(self):
        self._label = ""
        self._name = ""
        self._description = ""
        self._return_code = ReturnCode.ReturnCode()