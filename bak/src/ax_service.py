from typing import List
from .base_info import BaseInfo
from .owner import Owner
from .resource_requirement import ResourceRequirement
from .operating_system import OperatingSystem
from .message import Message
from .service_method import ServiceMethod


class AXService:
    def __init__(self, base_info: BaseInfo, owner: Owner, resource_requirements: ResourceRequirement,
                 operating_systems: List[OperatingSystem], messages: List[Message],
                 service_methods: List[ServiceMethod]):
        self.base_info = base_info
        self.owner = owner
        self.resource_requirements = resource_requirements
        self.operating_systems = operating_systems
        self.messages = messages
        self.service_methods = service_methods

    def __str__(self):
        return f"AXService(base_info={self.base_info}, owner={self.owner}, resource_requirements={self.resource_requirements}, operating_systems={self.operating_systems}, messages={self.messages}, service_methods={self.service_methods})"
