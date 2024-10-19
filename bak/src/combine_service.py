from typing import List
from .ax_service import AXService
from .atom_service import AtomService

class CombineService(AXService):
    def __init__(self, base_info, owner, resource_requirements, operating_systems, messages, service_methods, atom_service_list: List[AtomService]):
        super().__init__(base_info, owner, resource_requirements, operating_systems, messages, service_methods)
        self.atom_service_list = atom_service_list