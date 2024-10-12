import Message
import Capabilities
import ServiceMethod
class GrpcMethod(ServiceMethod.ServiceMethod):
    def __init__(self):
        self._requestMsg = Message.Message()
        self._responseMsg = Message.Message()
        self._capabilities = Capabilities.Capabilities()

    def toString(self):
        return f"Request Message: {self._requestMsg.toString()}, \
                Response Message: {self._responseMsg.toString()}, \
                Capabilities: {self._capabilities.toString()}"