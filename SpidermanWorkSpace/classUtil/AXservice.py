import BaseInfo
import Owner
import ResourceRequirement
import OperatingSystem
import Message

# baseinfo =  BaseInfo.BaseInfo()
# baseinfo.set_all_info("AXService", "AXService", "AXService", "1.0.0", "2022-01-01", 1, "MIT", "servicePath")
# print(baseinfo.description)

class AXservice:
    def __init__(self):
        self.__baseinfo = BaseInfo.BaseInfo() # private 
        self.__owner = Owner.Owner()
        self.__resource_requirement = ResourceRequirement.ResourceRequirement()
        self.__operating_system = OperatingSystem.OperatingSystem()
        self._message = []  # public
        self._service_method = [] # public

    def message_array(self, message):
        self._message.append(message)
    def service_method_array(self, service_method):
        self._service_method.append(service_method)

    def set_info(self, info):
        self.__baseinfo.set_info(info["baseinfo"])
        self.__owner.set_info(info["owner"])
        self.__resource_requirement.set_info(info["resource_requirement"])
        self.__operating_system.set_info(info["operating_system"])
        # self.__message.set_info(info["message"])
 
    def toString(self):
        print("BaseInfo: {}".format(self.__baseinfo.toString()))
        print("Owner: {}".format(self.__owner.toString()))
        print("Resource_Requirement: {}".format(self.__resource_requirement.toString()))
        print("Operating_System: {}".format(self.__operating_system.toString()))


# eg: test 
if __name__ == "__main__":
    axservice = AXservice()
    info = {
        "baseinfo": {
            "name": "AXService",
            "chinese_name": "AXService",
            "description": "AXService",
            "version": "1.0.0",
            "build_time": "2022-01-01",
            "priorty_level": 1,
            "license": "MIT",
            "servicePath": "servicePath"
        },
        "owner": {
            "mainter": {
                "name": "Mainter",
                "email": "mainter@example.com"
            },
            "developer": {
                "name": "Developer",
                "email": "developer@example.com"
            }
        },
        "resource_requirement": {
            "cpu_architecture": 1,
            "memory_size": 1,
            "hard_disk": 1
        },
        "operating_system": {
        "os_name": "OSName",
        "os_version": "OSVersion",
        "os_architecture": "OSArchitecture"
        }
    }

    axservice.set_info(info)
    print(axservice.toString())


