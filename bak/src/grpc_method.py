from .service_method import ServiceMethod
from .message import Message
from .capabilities import capabilities

class GrpcMethod(ServiceMethod):
    def __init__(self, name: str, chinese_name: str, description: str, return_code, requestMsg: Message, responseMsg: Message, capabilitiesVar: capabilities):
        super().__init__(name, chinese_name, description, return_code)
        self.requestMsg = requestMsg
        self.responseMsg = responseMsg
        self.capabilitiesVar = capabilitiesVar

    def __str__(self):
        return f"GrpcMethod(name={self.name}, requestMsg={self.requestMsg}, responseMsg={self.responseMsg}, capabilities={self.capabilitiesVar})"