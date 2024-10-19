from .ax_service import AXService
from .operating_system import OperatingSystem
import json

class ServiceUtil:
    def __init__(self, service: AXService, operating_system: OperatingSystem, program_language: str):
        self.service = service
        self.operating_system = operating_system
        self.program_language = program_language

    def parseCpp(self, fileName: str) -> bool:
        # Implement parsing logic
        return True

    def parseHpp(self, fileName: str) -> bool:
        # Implement parsing logic
        return True

    def loadJson(self, fileName: str) -> dict:
        with open(fileName, 'r') as file:
            return json.load(file)

    def writeCpp(self, filePath: str) -> bool:
        # Implement writing logic
        return True

    def writeHpp(self, filePath: str) -> bool:
        # Implement writing logic
        return True

    def generateJson(self, fileName: str) -> bool:
        # Implement generation logic
        return True