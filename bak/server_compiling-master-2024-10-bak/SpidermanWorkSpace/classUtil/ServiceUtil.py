import AXservice
import OperatingSystem

import json
class ServiceUtils:
    def __init__(self):
        self._axservice = AXservice.AXservice()
        self.__operating_system = OperatingSystem.OperatingSystem()
        self.__language = ""
    
    # @staticmethod
    # def generate_service_class_name(service_name: str) -> str:
    #     return f"{service_name.title()}Service"
    def parseCpp(self, fileName):
        # TODO: Parse the given C++ file and extract the necessary information

        with open(fileName, 'r') as file:
            lines = file.readlines()
        return lines
    
    def parseHpp(self, fileName):
        # TODO: Parse the given C++ header file and extract the necessary information

        with open(fileName, 'r') as file:
            lines = file.readlines()
        return lines
    
    def loadJson(self, fileName):
        # TODO: Load the given JSON file and populate the service object with the extracted information
        with open(fileName, 'r') as file:
            data = json.load(file)
            self._axservice.set_info(data)
    def writeCpp(self, fileName):
        # TODO: Write the  C++ code to the given file From Web_UI_tools
        # The generated code should include the AXservice and OperatingSystem classes,
        # and should use the extracted information to populate the objects

        # Example:
        # #include "AXservice.h"
        # #include "OperatingSystem.h"
        # 
        # AXservice axService;
        # OperatingSystem operatingSystem;
        # 
        # // Populate AXservice and OperatingSystem objects with the extracted information
        # axService.setInfo(extractedAXserviceInfo);
        # operatingSystem.setInfo(extractedOperatingSystemInfo);
        pass
    def writeHpp(self, fileName):
        # TODO: Write the  C++ header file to the given file From Web_UI_tools
        # The generated code should include the AXservice and OperatingSystem classes

        # Example:
        # // AXservice.h
        # #ifndef AXSERVICE_H
        # #define AXSERVICE_H
        # 
        # #include <iostream>
        # 
        # class AXservice {
        # public:
        #     void setInfo(const std::string& name, const std::string& description, const std::string& version,
        #                 const std::string& buildTime, int priortyLevel, const std::string& license,
        #                 const std::string& servicePath);
        # 
        #     std::string toString() const;
        # private:
        #     std::string name;
        #     std::string description;
        #     std::string version;
        #     std::string buildTime;
        #     int priortyLevel;
        pass

    def generateJson(self, jsonFileName):
        # TODO: Generate the JSON file from UI_tools
        data = {
            "baseinfo": "***",
            "owner": "***",
            "resource_requirement": "***",
            "operating_system": "***"
        }
        with open(jsonFileName, 'w') as file:
            json.dump(data, file, indent=4)
        print("JSON file generated successfully!")


    def generateCode(self, cppFileName, hppFileName, jsonFileName):
        # TODO: Generate the C++ code based on the extracted information from the C++ files, JSON file, and language
        print("C++ code generated successfully!")