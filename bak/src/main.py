from ax_service.ax_service import AXService
from ax_service.base_info import BaseInfo
from ax_service.owner import Owner
from ax_service.developer import Developer
from ax_service.maintainer import Maintainer
from ax_service.resource_requirement import ResourceRequirement
from ax_service.operating_system import OperatingSystem
from ax_service.message import Message
from ax_service.field import Field
from ax_service.service_method import ServiceMethod
from ax_service.return_code import ReturnCode
from ax_service.grpc_method import GrpcMethod
from ax_service.capabilities import capabilities

def main():
    # Example usage
    base_info = BaseInfo(name="ExampleService", chinese_name="示例服务", description="这是一个示例服务", version="1.0", build_time="2023-10-01", priority_level=1, license="MIT", servicePath="/example")
    developer = Developer(name="John Doe", email="john.doe@example.com")
    maintainer = Maintainer(name="Jane Doe", email="jane.doe@example.com")
    owner = Owner(developer=developer, maintainer=maintainer)
    resource_requirement = ResourceRequirement(cpu_architecture="x86_64", memory=4096, hard_disk=1024)
    operating_system = OperatingSystem(name="Linux", version="5.4.0")
    field1 = Field(id=1, name="field1", type="string", key="key1", value="value1", chinese_name="字段1")
    field2 = Field(id=2, name="field2", type="int", key="key2", value="value2", chinese_name="字段2")
    message = Message(label="request", name="RequestMessage", fields=[field1, field2])
    return_code = ReturnCode()
    return_code.addReturnValue("SUCCESS", 0)
    return_code.addReturnValue("ERROR", 1)
    service_method = ServiceMethod(name="exampleMethod", chinese_name="示例方法", description="这是一个示例方法", return_code=return_code)
    grpc_method = GrpcMethod(name="exampleGrpcMethod", chinese_name="示例gRPC方法", description="这是一个示例gRPC方法", return_code=return_code, requestMsg=message, responseMsg=message, capabilitiesVar=capabilities(read=True, write=True, delete=True))
    ax_service = AXService(base_info=base_info, owner=owner, resource_requirements=resource_requirement, operating_systems=[operating_system], messages=[message], service_methods=[service_method, grpc_method])

    print(ax_service)

if __name__ == "__main__":
    main()