import re
import json
from collections import defaultdict

from jinja2 import Template
import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
import AtomService
import OperatingSystem
from config.types import cpp_types


class ServiceUtil:
    def __init__(self):
        self._service = AtomService.AtomService()
        self._service_method_fun: str = []
        self.__operating_system = OperatingSystem.OperatingSystem()
        self.__language = ""

    # @staticmethod
    # def generate_service_class_name(service_name: str) -> str:
    #     return f"{service_name.title()}Service"

    def __type_convert(self):
        # 修改数据类型
        # 删除std::
        for message in self._service._messages:
            for field in message._fields:
                # field._type_proto为赋值时，才进行此操作
                if field._type_proto != "":
                    continue

                # 为 _type_proto 赋值
                field._type_proto = cpp_types.get(field._type, field._type)
                # 去除命名空间标示符
                if field._type_proto.count("std::") > 0:
                    field._type_proto = field._type_proto.replace("std::", "")

                # 数组转为repeated
                # vector
                if field._type_proto.count("vector") > 0:
                    field._repeated = True
                    # 使用正则表达式提取类型
                    match = re.search(r"vector<(\w+)>", field._type_proto)
                    temp_str = cpp_types.get(match.group(1), match.group(1))
                    if match:
                        field._type_proto = "repeated " + temp_str

                # []
                if field._name.count("[") > 0 and field._name.count("]") > 0:
                    field._repeated = True
                    field._type_proto = "repeated " + field._type_proto

                # map中的数据类型处理
                if field._type_proto.count("map") > 0:
                    field._map = True
                    match = re.search(r"map<(\w+),\s*(\w+)>", field._type_proto)
                    if match:
                        field._key = cpp_types.get(match.group(1), match.group(1))
                        field._value = cpp_types.get(match.group(2), match.group(2))
                        field._type_proto = f"map<{field._key}, {field._value}>"

    def __add_basic_info_dict(self, basic_info, key, value):
        basic_info_format_list = [
            "name",
            "description",
            "chinese_name",
            "version",
            "build_time",
            "priority_level",
            "license",
            "operating_system",
        ]
        if key == "file":
            basic_info["name"] = value.split(".")[0]
            return
        if key == "date":
            basic_info["build_time"] = value
            return
        if key == "priority_level":
            basic_info["priority_level"] = int(value)
            return
        if key in basic_info_format_list:
            basic_info[key] = value
            return

    def __extract_functions(self, file_content):
        # 匹配函数头部的正则表达式：支持类名、指针、引用、模板等复杂返回类型
        func_pattern = re.compile(
            r"\b[\w\s\*&<>:,\[\]]+\b\s+\w+\s*\([^)]*\)\s*{", re.MULTILINE
        )

        functions = []
        stack = []  # 用于处理嵌套大括号
        start = 0  # 用于记录函数起始位置

        # 找到所有函数头部位置
        for match in func_pattern.finditer(file_content):
            if not stack:  # 新函数起始
                start = match.start()
            stack.append("{")

            # 向后扫描，找到完整函数体
            for i in range(match.end(), len(file_content)):
                if file_content[i] == "{":
                    stack.append("{")
                elif file_content[i] == "}":
                    stack.pop()
                    if not stack:  # 栈为空，函数结束
                        functions.append(file_content[start : i + 1])
                        break

        return functions

    def parseCpp(self, fileName, encodings=None) -> list:
        # TODO: Parse the given C++ file and extract the necessary information
        if encodings is None:
            encodings = ["utf-8", "gbk", "latin1"]

        for encoding in encodings:
            try:
                with open(fileName, "r", encoding=encoding) as file:
                    content = file.read()
            except UnicodeDecodeError:
                continue

        # 删除单行注释
        content = re.sub(r"//.*$", "", content, flags=re.MULTILINE)

        # 正则表达式匹配函数定义
        # function_pattern = re.compile(r'(\w+\s+\w+\s*\([^)]*\)\s*\{[^}]*\})', re.DOTALL)
        # self._service_method_fun = function_pattern.findall(content)
        self._service_method_fun = self.__extract_functions(content)
        # print(self._service_method_fun)
        # 将解析的文件导入到框架内
        self._loadCpp(fileName)

        # return self._service_method_fun

    def parseHpp(self, fileName, encodings=None):
        # TODO: Parse the given C++ header file and extract the necessary information

        if encodings is None:
            encodings = ["utf-8", "gbk", "latin1"]

        for encoding in encodings:
            try:
                with open(fileName, "r", encoding=encoding) as file:
                    content = file.read()
            except UnicodeDecodeError:
                continue

        root_json_dict = dict()

        return_code = dict()
        """解析注释并构造字典结构。"""
        basic_info = dict()
        basic_info["owner"] = dict()
        lines = content.splitlines()
        # 过滤掉以 "//" 开头的行
        lines = [line for line in lines if not line.strip().startswith("//")]
        # 将过滤后的行重新组合成字符串
        lines = "\n".join(lines)
        lines = lines.splitlines()
        # print(lines)
        current_section = None
        operating_system_instance = dict()

        line_index = 0
        while line_index < len(lines):
            """
            解析注释
            """
            line = lines[line_index].strip()
            # print(line)
            # 解析以@开头的键值对
            if line[:5].count("@") > 0:
                parts = line[line.find("@") + 1 :].strip()
                # 使用正则表达式去除空格和冒号
                cleaned_line = re.sub(r"\s*:\s*", " ", parts)
                # 将字符串分为两个部分

                parts2 = cleaned_line.split(maxsplit=1)
                # print(parts2)
                if len(parts2) == 2:
                    key, value = parts2
                else:
                    key = parts2[0]
                    value = None

                if key in {
                    "resource_requirement",
                    "developer",
                    "maintainer",
                    "operating_system",
                }:
                    # 进入嵌套结构
                    current_section = key
                    if current_section in {"developer", "maintainer"}:
                        basic_info["owner"][current_section] = {}
                    elif current_section in {"operating_system"}:
                        basic_info["operating_system"] = []
                    else:
                        basic_info[current_section] = {}
                else:
                    # basic_info[key] = value
                    self.__add_basic_info_dict(basic_info, key, value)

            # 解析以+开头的嵌套键值对
            elif line.count("+") > 0 and current_section:
                nested_parts = line[1:].split(":", maxsplit=1)
                nested_key = nested_parts[0].strip()
                nested_key = nested_key.lstrip("+ ").strip()
                nested_value = nested_parts[1].strip() if len(nested_parts) > 1 else ""
                if current_section in {"developer", "maintainer"}:
                    basic_info["owner"][current_section][nested_key] = nested_value
                elif current_section in {"operating_system"}:
                    if nested_key == "name":
                        operating_system_instance = dict()
                        operating_system_instance[nested_key] = nested_value
                        operating_system_instance["version"] = {}
                        basic_info["operating_system"].append(operating_system_instance)
                    else:
                        basic_info["operating_system"][-1]["version"][
                            nested_key
                        ] = nested_value

                else:
                    basic_info[current_section][nested_key] = nested_value

            # 解析return_code
            elif line.startswith("#define") and line.count("<") == 0:
                return_parts = line[7:].strip()
                return_parts = return_parts.split(maxsplit=1)
                return_key = return_parts[0].strip()
                try:
                    return_value = return_parts[1].strip()
                    # print(return_value)
                except IndexError:
                    line_index += 1
                    continue
                return_code[return_key] = int(return_value)

            # 解析结构体
            elif line.startswith("typedef") or line.startswith("struct"):
                break
            line_index += 1

        """
        处理代码部分可能出现的注释，并将剩余代码合成一个大字符串
        """
        # 处理代码部分可能出现的注释
        for line in lines[line_index:]:
            if line.strip().startswith("/*") and line.strip().endswith("*/"):
                lines.remove(line)
        # 将其余的字符串从按行转为一个大字符串
        input_str = "\n".join(lines[line_index:])
        # 删除单行注释
        input_str = re.sub(r"//.*$", "", input_str, flags=re.MULTILINE)

        """
        解析结构体
        """
        # current_section = None
        # while line_index < len(lines):
        #     line = lines[line_index].strip()
        #
        #     if line.startswith('typedef') or line.startswith('struct'):
        #         current_section =
        # 使用正则表达式提取所有结构体的名称和字段
        # pattern = re.compile(r'typedef struct\s*\{(.*?)\}\s*(\w+);', re.DOTALL)
        pattern = re.compile(
            r"typedef\s+struct\s*(?:\w+\s*)?\{(.*?)\}\s*(\w+);", re.DOTALL
        )

        matches = pattern.finditer(input_str)
        # print(matches)
        struct_json_list = []

        for match in matches:
            fields_str = match.group(1).strip()
            struct_name = match.group(2)
            # print(fields_str,"\n\n")
            # 提取字段信息
            # field_pattern = re.compile(r'(\w+)\s+(\w+);')

            fields = []

            index = 1
            for field_match in fields_str.split("\n"):
                field_match = field_match.strip()
                if field_match == "" or field_match == None:
                    continue
                # print(field_match)
                field_list = field_match.rsplit(" ", 1)
                # print(field_list)
                field_type = field_list[0].strip()
                field_name = field_list[1].strip()
                if field_name[-1] == ";":
                    field_name = field_name[:-1].strip()
                # field_type = field_match.group(1)
                # field_name = field_match.group(2)
                # repeated

                # 序号
                fields.append({"id": index, "type": field_type, "name": field_name})
                index += 1

            # 构建 JSON 对象
            label = ""
            if "request" in struct_name.lower():
                label = "request"
            elif "reply" in struct_name.lower():
                label = "reply"

            json_obj = {"label": label, "name": struct_name, "fields": fields}
            struct_json_list.append(json_obj)

        """
        解析函数声明
        """
        # 正则表达式模式，用于匹配函数声明
        # pattern = re.compile(r'int\s+(\w+)\s*\(([^,]+)\s*\*\s*([^,]+)\s*,\s*([^,]+)\s*\*\s*([^,]+)\s*\);')
        pattern = re.compile(
            r"(?:\w+)\s+(\w+)\s*\(([^,]+)\s*\*\s*([^,]+)\s*,\s*([^,]+)\s*\*\s*([^,]+)\s*\);"
        )

        # 解析函数声明
        matches = pattern.findall(input_str)

        # 构建JSON格式的数据
        grpc_methods = []
        for match in matches:
            method_name = match[0]
            request_type = match[1].strip()
            response_type = match[3].strip()

            grpc_methods.append(
                {
                    "name": method_name,
                    "description": "ccccc",  # 这里可以根据需要修改描述
                    "requestMsg": request_type,
                    "responseMsg": response_type,
                    "capabilities": {"read": True, "write": False, "delete": False},
                }
            )

        root_json_dict["basic_info"] = basic_info
        root_json_dict["return_code"] = return_code
        root_json_dict["messages"] = struct_json_list
        root_json_dict["grpc_methods"] = grpc_methods

        # print(json.dumps(root_json_dict, indent=4))
        # 根据dict创建对象
        self._service = AtomService.AtomService()
        self._service.set_info(root_json_dict)

        # 整理message数据类型
        self.__type_convert()

        # 保存json到Json文件夹

        json_info = self._service.to_dict()
        with open(
            f"{os.path.dirname(os.path.abspath(__file__))}/../../Json/{self._service._base_info.getName()}.json",
            "w",
        ) as file:
            json.dump(json_info, file, indent=4)
            # print(root_json_dict)
        # 将解析的文件导入到框架内
        self._loadHpp(fileName)

    def loadJson(self, fileName):
        # TODO: Load the given JSON file and populate the service object with the extracted information
        with open(fileName, "r") as file:
            data = json.load(file)
            self._service.set_info(data)

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
            "operating_system": "***",
        }
        with open(jsonFileName, "w") as file:
            json.dump(data, file, indent=4)
        print("JSON file generated successfully!")

    def generateCode(self, cppFileName, hppFileName, jsonFileName):
        # TODO: Generate the C++ code based on the extracted information from the C++ files, JSON file, and language
        print("C++ code generated successfully!")

    def _loadCpp(self, cppFileName, encodings=None):
        if encodings is None:
            encodings = ["utf-8", "gbk", "latin1"]

        for encoding in encodings:
            try:
                with open(cppFileName, "r", encoding=encoding) as file:
                    content = file.read()
            except UnicodeDecodeError:
                continue

        # 定义正则表达式模式来匹配函数
        # function_pattern = re.compile(r'(\w+\s+\w+\s*\(.*?\)\s*\{.*?\})', re.DOTALL)

        # 查找所有匹配的函数
        # self._service_method_fun = function_pattern.findall(content)

        # 定义模板
        input_src_header_template = Template(
            open(
                f"{os.path.dirname(os.path.abspath(__file__))}/../../Jinja2/input_src_header_template.j2"
            ).read()
        )
        input_src_fun_template = Template(
            open(
                f"{os.path.dirname(os.path.abspath(__file__))}/../../Jinja2/input_src_fun_template.j2"
            ).read()
        )

        # 渲染模板
        res_str = ""
        input_src_header_str = input_src_header_template.render(
            service_name=self._service._base_info.getName()
        )
        res_str = res_str + input_src_header_str + "\n\n"

        for string in self._service_method_fun:
            res_str = res_str + string + "\n\n"

        for method in self._service._service_methods:
            func_name = method._name + "_func"
            request_type = method._requestMsg.get_name()
            reply_type = method._responseMsg.get_name()
            prim_func_name = method._name

            input_src_fun_str = input_src_fun_template.render(
                func_name=func_name,
                request_type=request_type,
                reply_type=reply_type,
                prim_func_name=prim_func_name,
            )
            res_str = res_str + input_src_fun_str + "\n\n"

        # 将res_str写入框架内的cpp文件中，同名不同路径
        with open(
            f"{os.path.dirname(os.path.abspath(__file__))}/../../atom_src/{self._service._base_info.getName()}.cpp",
            "w",
        ) as file:
            file.write(res_str)
        print(
            f"{os.path.dirname(os.path.abspath(__file__))}/../../atom_src/{self._service._base_info.getName()}.cpp generated successfully!"
        )

    def _loadHpp(self, hppFileName, encodings=None):
        if encodings is None:
            encodings = ["utf-8", "gbk", "latin1"]

        for encoding in encodings:
            try:
                with open(hppFileName, "r", encoding=encoding) as file:
                    lines = file.readlines()
            except UnicodeDecodeError:
                continue

        # 定义模板
        input_inc_fun_template = Template(
            open(
                f"{os.path.dirname(os.path.abspath(__file__))}/../../Jinja2/input_inc_fun_template.j2"
            ).read()
        )
        # 渲染模板
        res_str = ""
        for method in self._service._service_methods:
            func_name = method._name + "_func"
            request_type = method._requestMsg.get_name()
            reply_type = method._responseMsg.get_name()
            res_str += input_inc_fun_template.render(
                func_name=func_name, request_type=request_type, reply_type=reply_type
            )

        # 从后往前找到 #endif 的位置
        endif_index = -1
        for i in range(len(lines) - 1, -1, -1):
            if "#endif" in lines[i].strip():
                endif_index = i
                break

        if endif_index == -1:
            raise ValueError("文件中没有找到 #endif")

        # 在 #endif 之前插入字符串
        lines.insert(endif_index, res_str + "\n")

        # 将修改后的内容写回文件
        with open(
            f"{os.path.dirname(os.path.abspath(__file__))}/../../atom_inc/{self._service._base_info.getName()}.h",
            "w",
        ) as file:
            file.writelines(lines)
        print(
            f"{os.path.dirname(os.path.abspath(__file__))}/../../atom_inc/{self._service._base_info.getName()}.h generated successfully!"
        )

    # def generateSyncServerFile(self):
    #     proto_template = Template(open(f"{os.path.dirname(os.path.abspath(__file__))}/../../Jinja2/ClientMain_template.j2").read())

    #     res_str = proto_template.render(service_name = self.__service_name, service_name_package = self.__service_name_package, service_name_service = self.__service_name_service, service_name_interface=self.__service_name_interface, messages = self._messages, methods = self._service_methods)

    #     # 将res_str写入框架内的cpp文件中，同名不同路径
    #     with open(f"{os.path.dirname(os.path.abspath(__file__))}/../../rpc_server_inc/{self.__service_name}_impl.h", 'w') as file:
    #         file.write(res_str)
    #     print(f"{os.path.dirname(os.path.abspath(__file__))}/../../rpc_server_inc/{self.__service_name}_impl.h generated successfully!")
    #     pass

    # def generateAsynServerFile(self):
    #     pass

    # def _correctJson(self):
    #     res_dict =dict()
    #     res_dict[self._service._base_info.getName()] = dict()
    #     res_dict[self._service._base_info.getName()]["name"] = self._service._base_info.getName() +"service"
    #     res_dict[self._service._base_info.getName()]["description"] = self._service._base_info.getDescription()
    #     res_dict[self._service._base_info.getName()]["developer"] = dict()
    #     res_dict[self._service._base_info.getName()]["developer"]["name"] = self._service._owner.get_developer().get_name()
    #     res_dict[self._service._base_info.getName()]["developer"]["email"] = self._service._owner.get_developer().get_email()
    #     res_dict[self._service._base_info.getName()]["version"] = self._service._base_info.getVersion()
    #     res_dict[self._service._base_info.getName()]["build_time"] = self._service._base_info.getBuildTime()
    #     res_dict[self._service._base_info.getName()]["priority_level"] = self._service._base_info.getPriorityLevel()
    #     res_dict[self._service._base_info.getName()]["resource_requirements"] = dict()
    #     res_dict[self._service._base_info.getName()]["resource_requirements"]["cpu_architecture"] = self._service._resource_requirement.get_cpu_architecture()
    #     res_dict[self._service._base_info.getName()]["resource_requirements"]["hard_disk"] = self._service._resource_requirement.get_hard_disk()
    #     res_dict[self._service._base_info.getName()]["resource_requirements"]["memory"] = self._service._resource_requirement.get_memory_size()
    #     res_dict["implement_rpc"]= dict()
    #     res_dict["implement_rpc"]["syntax"] = "proto3"
    #     res_dict["implement_rpc"]["package"] = self._service._base_info.getName() + "_Package"
    #     res_dict["implement_rpc"]["service_name"] = self._service._base_info.getName() + "_Service"
    #     res_dict["implement_rpc"]["request"] = self._service._service_methods[0]._requestMsg.get_name()
    #     res_dict["implement_rpc"]["reply"] = self._service._service_methods[0]._responseMsg.get_name()
    #     res_dict["implement_rpc"]["atom_interface"] = self._service._service_methods[0]._name +"_func"
    #     res_dict["implement_rpc"]["atom_name"] = self._service._base_info.getName()

    #     res_dict["messages"] =list()
    #     res_dict["messages"].append(self._service._service_methods[0]._requestMsg.to_dict())
    #     res_dict["messages"].append(self._service._service_methods[0]._responseMsg.to_dict())
    #     res_dict["messages"][0]["lable"] = res_dict["messages"][0]["label"]
    #     del res_dict["messages"][0]["label"]
    #     res_dict["messages"][1]["lable"] = res_dict["messages"][1]["label"]
    #     del res_dict["messages"][1]["label"]
    #     for field in res_dict["messages"][0]["fields"]:
    #         field["type"] = field["type"].replace("std::","")
    #         if field["type"] == "int":
    #             field["type"] = "int32"
    #     for field in res_dict["messages"][1]["fields"]:
    #         field["type"] = field["type"].replace("std::","")
    #         if field["type"] == "int":
    #             field["type"] = "int32"

    #     res_dict["services"] =list()
    #     temp_dict =dict()
    #     temp_dict["name"] = self._service._base_info.getName() +"_Service"
    #     temp_dict["methods"] = list()
    #     temp_dict["methods"].append(self._service._service_methods[0].to_dict())
    #     temp_dict["methods"][0]["category"] = "user_management"
    #     temp_dict["methods"][0]["requestType"] = temp_dict["methods"][0]["requestMsg"]
    #     temp_dict["methods"][0]["responseType"] = temp_dict["methods"][0]["responseMsg"]
    #     del temp_dict["methods"][0]["requestMsg"]
    #     del temp_dict["methods"][0]["responseMsg"]
    #     res_dict["services"].append(temp_dict)

    #     # 保存json到Json文件夹
    #     with open(f"../../Json/{self._service._base_info.getName()}.json", 'w') as file:
    #         json.dump(res_dict, file, indent=4)
    #         print(f"../../Json/{self._service._base_info.getName()}.json generated successfully!")


if __name__ == "__main__":
    serviceUtils = ServiceUtil()
    # serviceUtils.parseHpp("test/atom_service_mbsb.h")
    # serviceUtils.parseHpp("D:\ZT\长安望江_服务化\code_demo\grpc-generate-server\\test\\atom_service_mbsb.h")
    # print("\n\n\n\n")
    # print(json.dumps(serviceUtils._service.to_dict(), indent=4))
    serviceUtilsA = ServiceUtil()
    serviceUtilsB = ServiceUtil()
    # serviceUtils.parseHpp("test/atom_service_mbsb.h")
    # serviceUtils.parseHpp("D:\ZT\长安望江_服务化\code_demo\grpc-generate-server\\test\\atom_service_mbsb.h")
    # print("\n\n\n\n")
    # print(json.dumps(serviceUtils._service.to_dict(), indent=4))
    serviceUtilsA.parseHpp("/root/grpc-generate-server/input_inc/atomic_service_mbsb.h")
    serviceUtilsA.parseCpp(
        "/root/grpc-generate-server/input_src/atomic_service_mbsb.cpp"
    )
    serviceUtilsB.parseHpp("/root/grpc-generate-server/input_inc/atomic_service_sf.h")
    serviceUtilsB.parseCpp("/root/grpc-generate-server/input_src/atomic_service_sf.c")

    # serviceUtilsA._correctJson()
    # serviceUtilsB._correctJson()
