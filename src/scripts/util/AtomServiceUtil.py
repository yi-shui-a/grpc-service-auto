import re
import json
from collections import defaultdict
from abc import abstractmethod
from jinja2 import Template
import sys
import os
import copy


from ..config import (
    cpp_proto_dict,
    cpp_idl_dict,
    service_task_suffix,
    Config,
    doc_types_correct_dict,
    doc_types_dict,
)
from ..entity import AtomService
from .Util import Util
from ..enums import FileEnum


class AtomServiceUtil:
    def __init__(self):
        pass
        # self._service_method_fun: str = []
        # self.__operating_system: OperatingSystem = OperatingSystem()
        # self.__language: str = ""

    # @staticmethod
    # def generate_service_class_name(service_name: str) -> str:
    #     return f"{service_name.title()}Service"

    @staticmethod
    def parseCpp(atom_service: AtomService, file_name: str, encodings=None):
        # TODO: Parse the given C++ file and extract the necessary information
        if encodings is None:
            encodings = ["utf-8", "gbk", "latin1"]

        for encoding in encodings:
            try:
                with open(file_name, "r", encoding=encoding) as file:
                    content = file.read()
            except UnicodeDecodeError:
                continue

        # 删除单行注释
        content = re.sub(r"//.*$", "", content, flags=re.MULTILINE)

        # 正则表达式匹配函数定义
        # content是CPP文件中删去注释后的所有内容
        # self._service_method_fun = self.__extract_functions(content)
        # 将解析的文件导入到框架内
        AtomServiceUtil._load_cpp(atom_service, file_name)

        # return self._service_method_fun

    @staticmethod
    def parseHpp(file_name, encodings=None) -> AtomService:
        # 读取文件到content
        if encodings is None:
            encodings = ["utf-8", "gbk", "latin1"]

        for encoding in encodings:
            try:
                with open(file_name, "r", encoding=encoding) as file:
                    content = file.read()
            except UnicodeDecodeError:
                continue

        """
        提取注释和微服务代码
        """
        # 构造正则表达式，匹配 begin_pattern 和 end_pattern 之间的内容（不区分大小写和空格）
        # 提取各个部分
        include_info = AtomServiceUtil.extract_section_hpp(
            content, r"/\*--.*?Include Begin.*?--\*/", r"/\*--.*?Include End.*?--\*/"
        )
        service_info = AtomServiceUtil.extract_section_hpp(
            content,
            r"/\*--.*?Service Info Begin.*?--\*/",
            r"/\*--.*?Service Info End.*?--\*/",
        )
        return_type_info = AtomServiceUtil.extract_section_hpp(
            content,
            r"/\*--.*?Return Type Begin.*?--\*/",
            r"/\*--.*?Return Type End.*?--\*/",
        )
        message_info = AtomServiceUtil.extract_section_hpp(
            content,
            r"/\*--.*?Message Info Begin.*?--\*/",
            r"/\*--.*?Message Info End.*?--\*/",
        )
        interface_declaration_info = AtomServiceUtil.extract_section_hpp(
            content,
            r"/\*--.*?Interface Declaration Begin.*?--\*/",
            r"/\*--.*?Interface Declaration End.*?--\*/",
        )
        # print(include_info)
        # print(service_info)
        # print(return_type_info)
        # print(message_info)
        # print(interface_declaration_info)
        # 检查是否成功提取到所有部分
        if include_info is None:
            print("Include Info not found")
            return None
        elif service_info is None:
            print("Service Info not found")
            return None
        elif return_type_info is None:
            print("Return Type Info not found")
            return None
        elif message_info is None:
            print("Message Info not found")
            return None
        elif interface_declaration_info is None:
            print("Interface Declaration Info not found")
            return None

        """
        提取注释信息
        """
        basic_info = dict()
        basic_info["owner"] = dict()
        current_key = None
        sub_dict = None
        sub_list = None

        # 按行处理
        for line in service_info.split("\n"):
            line = line.strip()
            # 去除行首星号、空格和注释符号
            line = re.sub(r"^\s*[\*\/]+\s*", "", line.strip())
            if not line:
                continue
            # 匹配 @key: value
            match_at = re.match(r"@(\w+):\s+(.+)$", line)
            if match_at:
                key = match_at.group(1).strip()
                value = match_at.group(2).strip().strip('"')
                basic_info[key] = value
                current_key = None  # 重置当前键
                continue

            # 匹配 @key:（无值，可能是子字典的开始）
            match_at_key_only = re.match(r"@(\w+):\s*$", line)
            if match_at_key_only:
                current_key = match_at_key_only.group(1).strip()
                # 如果是operating_system，初始化字典
                if current_key == "operating_system":
                    basic_info[current_key] = []
                    sub_list = basic_info[current_key]
                    continue
                basic_info[current_key] = {}  # 初始化子字典
                sub_dict = basic_info[current_key]
                continue

            # 匹配 +key: value（子字典的字段）
            match_plus = re.match(r"\+(\w+):\s*(.+)$", line)
            if match_plus and current_key and sub_dict is not None:
                sub_key = match_plus.group(1).strip()
                sub_value = match_plus.group(2).strip().strip('"')
                # 针对operating_system单独处理
                if current_key == "operating_system":
                    # 如果遇到name，结束当前字典并开始新的字典
                    if sub_key == "name":
                        sub_dict = dict()
                        sub_list.append(sub_dict)
                        sub_dict["os_name"] = sub_value
                        sub_dict["os_version"] = dict()
                    else:
                        sub_dict["os_version"][sub_key] = sub_value
                # 其他情况直接添加到子字典
                else:
                    sub_dict[sub_key] = sub_value
                continue

        # 移动maintainer和developer到owner
        if "maintainer" in basic_info:
            basic_info["owner"]["maintainer"] = basic_info.pop("maintainer")
        if "developer" in basic_info:
            basic_info["owner"]["developer"] = basic_info.pop("developer")
        # print(json.dumps(basic_info, indent=4))

        # 整理include信息，修正名称
        temp_dict = copy.deepcopy(basic_info)
        for key, value in temp_dict.items():
            if key in doc_types_correct_dict:
                basic_info[doc_types_correct_dict[key]] = basic_info.pop(key)
        for key, value in doc_types_dict.items():
            if basic_info.get(key, None) is None:
                basic_info[key] = value
        # 修正name字段为文件名，去除路径名和后缀
        basic_info["name"] = os.path.basename(file_name).split(".")[0]

        """
        提取return_type信息
        """
        return_code = dict()

        # 按行处理
        for line in return_type_info.split("\n"):
            line = line.strip()
            if not line:
                continue

            # 匹配 #define NAME VALUE
            match = re.match(r"#define\s+(\w+)\s+(\d+)", line)
            if match:
                name = match.group(1)
                value = int(match.group(2))
                return_code[name] = value

        """
        提取messages信息
        """
        messages = list()
        # 正则匹配结构体定义（支持多行和单行）
        message_info_pattern = re.compile(
            r"typedef\s+struct\s*{([^}]*)}[^{}]*?(\w+);",  # 匹配结构体定义
            re.DOTALL,  # 使 . 匹配换行符
        )

        # 匹配所有结构体
        message_info_matches = message_info_pattern.finditer(message_info)
        for match in message_info_matches:
            fields_text = match.group(1).strip()  # 字段定义部分
            struct_name = match.group(2).strip()  # 结构体名称

            # 解析字段
            fields = []
            field_id = 1
            # 字段行正则（忽略注释和空行）
            # field_line_pattern = re.compile(
            #     r"^\s*(?P<type>\w+)\s+(?P<name>\w+)\s*;.*$",  # 匹配 "type name;"
            #     re.MULTILINE,
            # )
            field_line_pattern = re.compile(
                r"""
                (?:const\s+)?                          # const限定符
                (?:std::)?                             # std命名空间
                (?:\w+<.*?>|\w+(?:\s*\*\s*)?)          # 模板类型或普通类型（可能带指针）
                (?:\s*$$\s*\d*\s*$$)?                  # 数组维度
                \s+                                    # 分隔空格
                (\w+)                                  # 变量名
                \s*;                                   # 结束分号
                """,
                re.VERBOSE,
            )

            # 逐行处理字段定义
            for line in fields_text.split("\n"):
                line = line.strip()
                if not line or line.startswith("//"):
                    continue

                # 尝试匹配类型声明
                type_match = field_line_pattern.search(line)
                if type_match:
                    full_type = line.split(";")[0].strip()  # 获取完整类型声明
                    var_name = type_match.group(1)

                    fields.append(
                        {
                            "id": field_id,
                            "name": var_name,
                            "type": " ".join(full_type.split(" ")[:-1]),
                            "description": "",
                            "chinese_name": "",
                        }
                    )
                    field_id += 1

            messages.append({"name": struct_name, "description": "", "fields": fields})

            # for field_match in field_line_pattern.finditer(fields_text):
            #     field_type = field_match.group(1)
            #     field_name = field_match.group(2)

            #     fields.append(
            #         {
            #             "id": field_id,
            #             "name": field_name,
            #             "description": "",
            #             "type": field_type,
            #             "chinese_name": "",
            #         }
            #     )
            #     field_id += 1

            # # 添加到结果
            # messages.append({"name": struct_name, "description": "", "fields": fields})

        """
        提取interface_declarations信息
        """
        interface_declarations = list()

        # 去除所有除空格外以//开头的行
        interface_declaration_info = re.sub(
            r"^//.*$", "", interface_declaration_info, flags=re.MULTILINE
        )

        pattern = re.compile(
            r"(?:\w+)\s+(\w+)\s*\(([^,]+)\s*\*\s*([^,]+)\s*,\s*([^,]+)\s*\*\s*([^,]+)\s*\);"
        )

        # 解析函数声明
        matches = pattern.findall(interface_declaration_info)

        # 构建JSON格式的数据
        for match in matches:
            method_name = match[0]
            request_type = match[1].strip()
            response_type = match[3].strip()

            interface_declarations.append(
                {
                    "name": method_name,
                    "description": "ccccc",  # 这里可以根据需要修改描述
                    "requestMsg": request_type,
                    "responseMsg": response_type,
                    "capabilities": {"read": True, "write": False, "delete": False},
                }
            )

        """
        整理数据生成AtomService
        """
        atom_service_dict = dict()
        atom_service_dict["basic_info"] = basic_info
        atom_service_dict["return_code"] = return_code
        atom_service_dict["messages"] = messages
        atom_service_dict["methods"] = interface_declarations
        # print(json.dumps(atom_service_dict, indent=4))
        atom_service = AtomService()
        atom_service.set_info(atom_service_dict)
        # 整理message数据类型
        AtomServiceUtil.__type_convert(atom_service)

        # 保存json到Json文件夹
        json_info = atom_service.to_dict()
        # 转为json字符串格式
        Util.saveFile(
            [atom_service._base_info.get_name()],
            json.dumps(json_info, indent=4),
            FileEnum.ATOM_SERIVCE_JSON,
        )
        # with open("test.json", "w") as file:
        #     json.dump(json_info, file, indent=4)
        # 将解析前的原文件再次导入到框架内
        AtomServiceUtil._loadHpp(atom_service, file_name)
        return atom_service

    @staticmethod
    def _loadHpp(atom_service: AtomService, hpp_file_name: str, encodings=None):
        """
        This function reads a C++ header file, identifies the service methods, and generates
        a new C++ header file with additional function declarations for each method.

        Parameters:
        - atom_service (AtomService): An instance of the AtomService class representing the service.
        - hpp_file_name (str): The name of the C++ header file to be processed.
        - encodings (list, optional): A list of encodings to try when reading the file. Defaults to ["utf-8", "gbk", "latin1"].

        Returns:
        None. The function prints a success message if the new C++ header file is generated successfully.
        """
        if encodings is None:
            encodings = ["utf-8", "gbk", "latin1"]

        # 读取原文件
        for encoding in encodings:
            try:
                with open(hpp_file_name, "r", encoding=encoding) as file:
                    lines = file.readlines()
            except UnicodeDecodeError:
                continue

        # 定义模板
        input_include_fun_template = Template(
            open(
                f"{os.path.dirname(os.path.abspath(__file__))}/../../templates/input_process_template/input_include_fun_template.j2"
            ).read()
        )
        # 渲染模板
        res_str = ""
        for method in atom_service._service_methods:
            func_name = method._name + service_task_suffix
            request_type = method._requestMsg.get_name()
            reply_type = method._responseMsg.get_name()
            res_str += input_include_fun_template.render(
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
        Util.saveFile(
            name_list=[atom_service._base_info.get_name()],
            content="".join(lines),
            type=FileEnum.HPP,
        )
        # if not os.path.isdir(
        #     f"{os.path.dirname(os.path.abspath(__file__))}/../../../db/atomic_service/{atom_service._base_info.get_name()}/atomic_include"
        # ):
        #     os.makedirs(
        #         f"{os.path.dirname(os.path.abspath(__file__))}/../../../db/atomic_service/{atom_service._base_info.get_name()}/atomic_include"
        #     )

        # with open(
        #     f"{os.path.dirname(os.path.abspath(__file__))}/../../../db/atomic_service/{atom_service._base_info.get_name()}/atomic_include/{atom_service._base_info.get_name()}.h",
        #     "w",
        # ) as file:
        #     file.writelines(lines)
        # print(
        #     f"{os.path.dirname(os.path.abspath(__file__))}/../../../db/atomic_service/{atom_service._base_info.get_name()}/atomic_include/{atom_service._base_info.get_name()}.h generated successfully!"
        # )

    @staticmethod
    def _load_cpp(atom_service: AtomService, cpp_file_name, encodings=None):
        if encodings is None:
            encodings = ["utf-8", "gbk", "latin1"]

        for encoding in encodings:
            try:
                with open(cpp_file_name, "r", encoding=encoding) as file:
                    content = file.read()
            except UnicodeDecodeError:
                continue

        # 删除带有include引用库语句的代码行
        content = re.sub(
            r'^\s*#include\s*[<"].*?[>"]\s*$', "", content, flags=re.MULTILINE
        )

        content = content + "\n\n\n"

        # 定义模板
        input_src_header_template = Template(
            open(
                f"{os.path.dirname(os.path.abspath(__file__))}/../../templates/input_process_template/input_src_header_template.j2"
            ).read()
        )
        input_src_fun_template = Template(
            open(
                f"{os.path.dirname(os.path.abspath(__file__))}/../../templates/input_process_template/input_src_fun_template.j2"
            ).read()
        )

        # 渲染模板
        res_str = ""
        input_src_header_str = input_src_header_template.render(
            service_name=atom_service._base_info.get_name()
        )
        # 添加模版内容
        res_str = res_str + input_src_header_str + "\n\n"

        # for string in self._service_method_fun:
        #     res_str = res_str + string + "\n\n"

        # 添加原CPP文件
        res_str = res_str + content

        # 添加封装后的方法
        for method in atom_service._service_methods:
            func_name = method._name + service_task_suffix
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
        Util.saveFile(
            name_list=[atom_service._base_info.get_name()],
            content=res_str,
            type=FileEnum.CPP,
        )
        # if not os.path.isdir(
        #     f"{os.path.dirname(os.path.abspath(__file__))}/../../../db/atomic_service/{atom_service._base_info.get_name()}/atomic_src"
        # ):
        #     os.makedirs(
        #         f"{os.path.dirname(os.path.abspath(__file__))}/../../../db/atomic_service/{atom_service._base_info.get_name()}/atomic_src"
        #     )

        # with open(
        #     f"{os.path.dirname(os.path.abspath(__file__))}/../../../db/atomic_service/{atom_service._base_info.get_name()}/atomic_src/{atom_service._base_info.get_name()}.cpp",
        #     "w",
        # ) as file:
        #     file.write(res_str)
        # print(
        #     f"{os.path.dirname(os.path.abspath(__file__))}/../../../db/atomic_service/{atom_service._base_info.get_name()}/atomic_src/{atom_service._base_info.get_name()}.cpp generated successfully!"
        # )

    @staticmethod
    def generateAtomServiceCMakeLists(atom_service: AtomService):
        service_name = atom_service._base_info.get_name()
        proto_template = Template(
            open(
                f"{os.path.dirname(os.path.abspath(__file__))}/../../templates/input_process_template/atomic_src_compile_cmake.j2"
            ).read()
        )
        res_str = proto_template.render(service_name=service_name)

        Util.saveFile(
            name_list=[service_name], content=res_str, type=FileEnum.CPP_CMAKE
        )
        # # 确保目录存在
        # os.makedirs(
        #     f"{os.path.dirname(os.path.abspath(__file__))}/../../../db/atomic_service/{service_name}/atomic_src/",
        #     exist_ok=True,
        # )

        # # 将res_str写入框架内的cpp文件中，同名不同路径
        # with open(
        #     f"{os.path.dirname(os.path.abspath(__file__))}/../../../db/atomic_service/{service_name}/atomic_src/CMakeLists.txt",
        #     "w",
        # ) as file:
        #     file.write(res_str)
        # print(
        #     f"{os.path.dirname(os.path.abspath(__file__))}/../../../db/atomic_service/{service_name}/atomic_src/CMakeLists.txt generated successfully!"
        # )

    @staticmethod
    def __type_convert(atom_service: AtomService):
        # 修改数据类型
        # 删除std::
        for message in atom_service._messages:
            for field in message._fields:
                # field._type_proto为赋值时，才进行此操作
                # if field._type_proto != "":
                #     continue
                """
                处理protoBuffer类型的数据
                """
                # 为 _type_proto 赋值
                # field._type_proto = cpp_proto_dict.get(field._type, field._type)
                field._type_proto = field._type
                # 去除命名空间标示符
                if field._type_proto.count("std::") > 0:
                    field._type_proto = field._type_proto.replace("std::", "")

                field._type_proto = cpp_proto_dict.get(
                    field._type_proto, field._type_proto
                )

                # 数组转为repeated
                # vector
                if field._type_proto.count("vector") > 0:
                    field._repeated = True
                    # 使用正则表达式提取类型
                    match = re.search(r"vector<(\w+)>", field._type_proto)
                    temp_str = cpp_proto_dict.get(match.group(1), match.group(1))
                    if match:
                        field._type_proto = "repeated " + temp_str

                # 处理[]
                if field._name.count("[") > 0 and field._name.count("]") > 0:
                    field._repeated = True
                    field._type_proto = "repeated " + field._type_proto

                # map中的数据类型处理
                if field._type_proto.count("map") > 0:
                    field._map = True
                    match = re.search(r"map<(\w+),\s*(\w+)>", field._type_proto)
                    if match:
                        field._key = cpp_proto_dict.get(match.group(1), match.group(1))
                        field._value = cpp_proto_dict.get(
                            match.group(2), match.group(2)
                        )
                        field._type_proto = f"map<{field._key}, {field._value}>"

                """
                处理idl类型的数据
                """
                field._type_idl = field._type
                # 去除命名空间标示符
                if field._type_idl.count("std::") > 0:
                    field._type_idl = field._type_idl.replace("std::", "")

                field._type_idl = cpp_idl_dict.get(field._type_idl, field._type_idl)



    @staticmethod
    def extract_section_hpp(content, begin_pattern, end_pattern):
        # 构造正则表达式，匹配 begin_pattern 和 end_pattern 之间的内容（不区分大小写和空格）

        # pattern = re.compile(
        #     rf"^{begin_pattern}.*?$\n(.*?)^{end_pattern}.*?$",
        #     re.DOTALL | re.IGNORECASE | re.MULTILINE,
        # )
        pattern = re.compile(
            rf"^{begin_pattern}.*?$(.*?)^{end_pattern}.*?$",
            re.DOTALL | re.IGNORECASE | re.MULTILINE,
        )

        match = pattern.search(content)
        if match:
            return match.group(1).strip()  # 返回匹配的内容，并去除前后空白
        return None

    @staticmethod
    def compileAtomService(atom_service: AtomService):
        """
        自动生成 AtomService 源文件的静态链接库

        :param atom_service: AtomService 对象
        :return: None
        """
        service_name = atom_service._base_info.get_name()
        proto_dir = f"{os.path.dirname(os.path.abspath(__file__))}/../../../db/atomic_service/{atom_service._base_info.get_name()}/atomic_src/"

        Util.compileCmakeProject(proto_dir, service_name, file_type="cpp")

    @staticmethod
    def loadAtomService(json_file: str) -> AtomService:
        """
        读取json文件，生成AtomService对象
        """
        # 读取json文件
        with open(json_file, "r") as file:
            json_data = json.load(file)
        # 创建AtomService对象
        atom_service = AtomService()
        atom_service.set_info(json_data)
        return atom_service
    
    def getAtomServiceJson(service_name:str)->dict:
        """
        读取json文件，生成AtomService对象
        """
        # 读取json文件
        with open(f"{os.path.dirname(os.path.abspath(__file__))}/../../../db/atomic_service/{service_name}/{service_name}.json", "r") as file:
            json_data = json.load(file)
        return json_data

    # 获取CPP文件中完整的函数体组成的列表
    @staticmethod
    def __extract_functions(file_content):
        # # content是CPP文件中删去注释后的所有内容
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
    
    
        @staticmethod
        def __add_basic_info_dict(basic_info, key, value):
            basic_info_format_list = [
                "name",
                "description",
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
            if key == "chinese_name":
                value = value.replace('"', "")
                basic_info["chinese_name"] = value
                return
            if key in basic_info_format_list:
                basic_info[key] = value
            return

    # @staticmethod
    # def parseHpp_old(file_name, encodings=None) -> AtomService:
    #     # TODO: Parse the given C++ header file and extract the necessary information

    #     if encodings is None:
    #         encodings = ["utf-8", "gbk", "latin1"]

    #     for encoding in encodings:
    #         try:
    #             with open(file_name, "r", encoding=encoding) as file:
    #                 content = file.read()
    #         except UnicodeDecodeError:
    #             continue

    #     """提取信息"""
    #     content_lines = []
    #     # 提取包含防护
    #     include_guard_pattern = re.compile(
    #         r"#ifndef\s+(\w+)\s+#define\s+\1", re.MULTILINE
    #     )
    #     include_guard_match = include_guard_pattern.search(content)
    #     if include_guard_match:
    #         content_lines.append(f"#ifndef {include_guard_match.group(1)}")
    #         content_lines.append(f"#define {include_guard_match.group(1)}")

    #     # 提取每对 Begin 和 End 之间的内容
    #     # 使用非贪婪模式 .*? 以确保匹配到最近的 End 注释
    #     section_pattern = re.compile(
    #         r"/\*[-]+\s*(.*?)\s*Begin\s*[-]+\*/\s*(.*?)\s*/\*[-]+\s*\1\s*End\s*[-]+\*/",
    #         re.DOTALL,
    #     )
    #     for match in section_pattern.finditer(content):
    #         content_lines.append(match.group(0))

    #     # 提取 #endif
    #     endif_pattern = re.compile(r"#endif\s*//\s*(\w+)", re.MULTILINE)
    #     endif_match = endif_pattern.search(content)
    #     if endif_match:
    #         content_lines.append(f"#endif // {endif_match.group(1)}")

    #     content_lines = "\n".join(content_lines)

    #     root_json_dict = dict()

    #     return_code = dict()
    #     """解析注释并构造字典结构。"""
    #     basic_info = dict()
    #     basic_info["owner"] = dict()
    #     lines = content_lines.splitlines()
    #     # 过滤掉以 "//" 开头的行
    #     lines = [line for line in lines if not line.strip().startswith("//")]
    #     # 将过滤后的行重新组合成字符串
    #     lines = "\n".join(lines)
    #     lines = lines.splitlines()
    #     # print(lines)
    #     current_section = None
    #     operating_system_instance = dict()
    #     # 各部分状态信息
    #     # include_state = False
    #     # service_info_state = False
    #     # return_type_state = False
    #     # message_info_state = False
    #     # interface_declaration = False
    #     # 存储解析状态的栈
    #     state = []
    #     include_state = "INCLUDE"
    #     service_info_state = "SERVICE_INFO"
    #     return_type_state = "RETURN_TYPE"
    #     message_info_state = "MESSAGE_INFO"
    #     interface_declaration_state = "INTERFACE_DECLARATION"

    #     # 存储结构体内容和接口声明内容
    #     message_info = []
    #     interface_declaration = []

    #     # 正则表达式模式
    #     include_pattern = re.compile(r"include", re.MULTILINE)

    #     service_info_pattern = re.compile(r"service\s*info", re.MULTILINE)

    #     return_type_pattern = re.compile(r"return\s*type", re.MULTILINE)

    #     message_info_pattern = re.compile(r"message\s*info", re.MULTILINE)

    #     interface_declaration_pattern = re.compile(
    #         r"interface\s*declaration", re.MULTILINE
    #     )

    #     line_index = 0
    #     while line_index < len(lines):
    #         line = lines[line_index].strip()
    #         """获取解析状态"""
    #         # begin正则表达式模式
    #         begin_pattern = re.compile(
    #             r"/\*[-]+\s*(.*?)\s*Begin\s*[-]+\*/", re.DOTALL | re.IGNORECASE
    #         )
    #         begin_match = begin_pattern.search(line)
    #         if begin_match:
    #             begin = begin_match.group(1).strip().lower()

    #             include_begin_match = include_pattern.search(begin)
    #             service_info_begin_match = service_info_pattern.search(begin)
    #             return_type_begin_match = return_type_pattern.search(begin)
    #             message_info_begin_match = message_info_pattern.search(begin)
    #             interface_declaration_begin_match = (
    #                 interface_declaration_pattern.search(begin)
    #             )

    #             if include_begin_match:
    #                 state.append(include_state)
    #             elif service_info_begin_match:
    #                 state.append(service_info_state)
    #             elif return_type_begin_match:
    #                 state.append(return_type_state)
    #             elif message_info_begin_match:
    #                 state.append(message_info_state)
    #             elif interface_declaration_begin_match:
    #                 state.append(interface_declaration_state)

    #         if len(state) != 0:
    #             """解析注释"""
    #             state_now = state.pop()
    #             state.append(state_now)
    #             if state_now == service_info_state:
    #                 # print(line)
    #                 # 解析以@开头的键值对
    #                 if line[:5].count("@") > 0:
    #                     parts = line[line.find("@") + 1 :].strip()
    #                     # 使用正则表达式去除空格和冒号
    #                     cleaned_line = re.sub(r"\s*:\s*", " ", parts)
    #                     # 将字符串分为两个部分

    #                     parts2 = cleaned_line.split(maxsplit=1)
    #                     # print(parts2)
    #                     if len(parts2) == 2:
    #                         key, value = parts2
    #                     else:
    #                         key = parts2[0]
    #                         value = None

    #                     if key in {
    #                         "resource_requirement",
    #                         "developer",
    #                         "maintainer",
    #                         "operating_system",
    #                     }:
    #                         # 进入嵌套结构
    #                         current_section = key
    #                         if current_section in {"developer", "maintainer"}:
    #                             basic_info["owner"][current_section] = {}
    #                         elif current_section in {"operating_system"}:
    #                             basic_info["operating_system"] = []
    #                         else:
    #                             basic_info[current_section] = {}
    #                     else:
    #                         # basic_info[key] = value
    #                         AtomServiceUtil.__add_basic_info_dict(
    #                             basic_info, key, value
    #                         )

    #                 # 解析以+开头的嵌套键值对
    #                 elif line.count("+") > 0 and current_section:
    #                     nested_parts = line[1:].split(":", maxsplit=1)
    #                     nested_key = nested_parts[0].strip()
    #                     nested_key = nested_key.lstrip("+ ").strip()
    #                     nested_value = (
    #                         nested_parts[1].strip() if len(nested_parts) > 1 else ""
    #                     )
    #                     if current_section in {"developer", "maintainer"}:
    #                         basic_info["owner"][current_section][
    #                             nested_key
    #                         ] = nested_value
    #                     elif current_section in {"operating_system"}:
    #                         if nested_key == "name":
    #                             operating_system_instance = dict()
    #                             operating_system_instance[nested_key] = nested_value
    #                             operating_system_instance["version"] = {}
    #                             basic_info["operating_system"].append(
    #                                 operating_system_instance
    #                             )
    #                         else:
    #                             basic_info["operating_system"][-1]["version"][
    #                                 nested_key
    #                             ] = nested_value

    #                     else:
    #                         basic_info[current_section][nested_key] = nested_value

    #             """解析return_code"""
    #             if state_now == return_type_state:

    #                 if line.startswith("#define") and line.count("<") == 0:
    #                     return_parts = line[7:].strip()
    #                     return_parts = return_parts.split(maxsplit=1)
    #                     return_key = return_parts[0].strip()
    #                     try:
    #                         return_value = return_parts[1].strip()
    #                         # print(return_value)
    #                     except IndexError:
    #                         line_index += 1
    #                         continue
    #                     return_code[return_key] = int(return_value)

    #             """解释结构体"""
    #             if state_now == message_info_state:
    #                 message_info.append(line)

    #             if state_now == interface_declaration_state:
    #                 interface_declaration.append(line)

    #             """更新解析状态"""
    #             # end正则表达式模式
    #             end_pattern = re.compile(
    #                 r"/\*[-]+\s*(.*?)\s*End\s*[-]+\*/", re.DOTALL | re.IGNORECASE
    #             )
    #             end_match = end_pattern.search(line)
    #             if end_match:
    #                 end = end_match.group(1).strip().lower()

    #                 include_end_match = include_pattern.search(end)
    #                 service_info_end_match = service_info_pattern.search(end)
    #                 return_type_end_match = return_type_pattern.search(end)
    #                 message_info_end_match = message_info_pattern.search(end)
    #                 interface_declaration_end_match = (
    #                     interface_declaration_pattern.search(end)
    #                 )

    #                 state_now = state.pop()

    #                 if include_end_match:
    #                     if state_now != include_state:
    #                         print("CONTENT ERROR BETWEEN BEGIN AND AND")
    #                 elif service_info_end_match:
    #                     if state_now != service_info_state:
    #                         print("CONTENT ERROR BETWEEN BEGIN AND AND")
    #                 elif return_type_end_match:
    #                     if state_now != return_type_state:
    #                         print("CONTENT ERROR BETWEEN BEGIN AND AND")
    #                 elif message_info_end_match:
    #                     if state_now != message_info_state:
    #                         print("CONTENT ERROR BETWEEN BEGIN AND AND")
    #                 elif interface_declaration_end_match:
    #                     if state_now != interface_declaration_state:
    #                         print("CONTENT ERROR BETWEEN BEGIN AND AND")
    #                 else:
    #                     state.append(state_now)

    #         line_index += 1

    #     message_info = "\n".join(message_info)
    #     # 删除单行注释
    #     message_info = re.sub(r"//.*$", "", message_info, flags=re.MULTILINE)
    #     interface_declaration = "\n".join(interface_declaration)
    #     # 删除单行注释
    #     interface_declaration = re.sub(
    #         r"//.*$", "", interface_declaration, flags=re.MULTILINE
    #     )

    #     """
    #     解析结构体
    #     """

    #     """解析typedef struct开头的结构体"""
    #     pattern = re.compile(
    #         r"typedef\s+struct\s*(?:\w+\s*)?\{(.*?)\}\s*(\w+);", re.DOTALL
    #     )

    #     matches = pattern.finditer(message_info)
    #     # print(matches)
    #     struct_json_list = []

    #     for match in matches:
    #         fields_str = match.group(1).strip()
    #         struct_name = match.group(2)
    #         # print(fields_str,"\n\n")
    #         # 提取字段信息
    #         # field_pattern = re.compile(r'(\w+)\s+(\w+);')

    #         fields = []

    #         index = 1
    #         for field_match in fields_str.split("\n"):
    #             field_match = field_match.strip()
    #             if field_match == "" or field_match == None:
    #                 continue
    #             # print(field_match)
    #             field_list = field_match.rsplit(" ", 1)
    #             # print(field_list)
    #             field_type = field_list[0].strip()
    #             field_name = field_list[1].strip()
    #             if field_name[-1] == ";":
    #                 field_name = field_name[:-1].strip()
    #             # field_type = field_match.group(1)
    #             # field_name = field_match.group(2)
    #             # repeated

    #             # 序号
    #             fields.append({"id": index, "type": field_type, "name": field_name})
    #             index += 1

    #         # 构建 JSON 对象
    #         label = ""
    #         if "request" in struct_name.lower():
    #             label = "request"
    #         elif "reply" in struct_name.lower():
    #             label = "reply"

    #         json_obj = {"label": label, "name": struct_name, "fields": fields}
    #         struct_json_list.append(json_obj)

    #     """解析struct开头的结构体"""
    #     lines_struct = message_info.splitlines()
    #     in_struct = False
    #     end = False
    #     struct_lines = []

    #     for line in lines_struct:
    #         line = line.strip()
    #         if line.startswith("struct"):
    #             # 进入 struct 收集状态
    #             in_struct = True

    #         if in_struct:
    #             struct_lines.append(line)

    #         if in_struct and re.search(r"\}", line):
    #             end = True

    #         # 当这一行以分号 ';' 结尾时，说明 struct 定义结束
    #         if in_struct and end and line.endswith(";"):
    #             # 将所有收集的行合并成一行去解析
    #             block = " ".join(struct_lines)
    #             # 先简单合并多余空白
    #             block = " ".join(block.split())

    #             # 移除开头的 'struct '
    #             if block.startswith("struct "):
    #                 block = block[len("struct ") :]

    #             # 找到第一对花括号
    #             brace_start = block.find("{")
    #             if brace_start == -1:
    #                 continue  # 不符合期望格式

    #             # 在花括号之前，可能有 struct 的名字
    #             name_part = block[:brace_start].strip()

    #             # 找到与之匹配的 '}'
    #             brace_end = block.find("}", brace_start)
    #             if brace_end == -1:
    #                 continue

    #             fields = []
    #             # 解析花括号内的所有字段
    #             fields_str = block[brace_start + 1 : brace_end].strip()
    #             # 按分号拆分每个字段
    #             field_lines = fields_str.split(";")
    #             index = 1
    #             for f in field_lines:
    #                 if f == "":
    #                     continue
    #                 f = f.strip()
    #                 f_list = f.split(" ")
    #                 field_type = f_list[0].strip()
    #                 field_name = f_list[1].strip()
    #                 # 序号
    #                 fields.append({"id": index, "type": field_type, "name": field_name})
    #                 index += 1

    #             # # 花括号之后到最后的结构体变量部分
    #             # alias_part = block[brace_end + 1:].strip()
    #             # if alias_part.endswith(';'):
    #             #     alias_part = alias_part[:-1].strip()
    #             # # 如果有多个结构体变量，就用逗号分隔
    #             # if alias_part:
    #             #     aliases = [x.strip() for x in alias_part.split(',')]

    #             # 构建 JSON 对象
    #             label = ""
    #             if "request" in name_part.lower():
    #                 label = "request"
    #             elif "reply" in name_part.lower():
    #                 label = "reply"

    #             json_obj = {"label": label, "name": name_part, "fields": fields}
    #             struct_json_list.append(json_obj)

    #             # 重置收集状态
    #             struct_lines = []
    #             in_struct = False
    #             end = False

    #     """
    #     解析函数声明
    #     """
    #     # 正则表达式模式，用于匹配函数声明
    #     # pattern = re.compile(r'int\s+(\w+)\s*\(([^,]+)\s*\*\s*([^,]+)\s*,\s*([^,]+)\s*\*\s*([^,]+)\s*\);')
    #     pattern = re.compile(
    #         r"(?:\w+)\s+(\w+)\s*\(([^,]+)\s*\*\s*([^,]+)\s*,\s*([^,]+)\s*\*\s*([^,]+)\s*\);"
    #     )

    #     # 解析函数声明
    #     matches = pattern.findall(interface_declaration)

    #     # 构建JSON格式的数据
    #     methods = []
    #     for match in matches:
    #         method_name = match[0]
    #         request_type = match[1].strip()
    #         response_type = match[3].strip()

    #         methods.append(
    #             {
    #                 "name": method_name,
    #                 "description": "ccccc",  # 这里可以根据需要修改描述
    #                 "requestMsg": request_type,
    #                 "responseMsg": response_type,
    #                 "capabilities": {"read": True, "write": False, "delete": False},
    #             }
    #         )

    #     root_json_dict["basic_info"] = basic_info
    #     root_json_dict["return_code"] = return_code
    #     root_json_dict["messages"] = struct_json_list
    #     root_json_dict["methods"] = methods

    #     # print(json.dumps(root_json_dict, indent=4))
    #     # 根据dict创建对象
    #     # 创建一个AtomService变量
    #     atom_service = AtomService()
    #     atom_service.set_info(root_json_dict)
    #     # print(json.dumps(atom_service.to_dict(), indent=4))
    #     # 整理message数据类型
    #     AtomServiceUtil.__type_convert(atom_service)

    #     # 保存json到Json文件夹
    #     json_info = atom_service.to_dict()
    #     # 转为json字符串格式
    #     Util.saveFile(
    #         [atom_service._base_info.get_name()],
    #         json.dumps(json_info, indent=4),
    #         FileEnum.ATOM_SERIVCE_JSON,
    #     )
    #     # 确保目录存在
    #     # os.makedirs(
    #     #     f"{os.path.dirname(os.path.abspath(__file__))}/../../../db/atomic_service/{atom_service._base_info.get_name()}",
    #     #     exist_ok=True,
    #     # )

    #     # with open(
    #     #     f"{os.path.dirname(os.path.abspath(__file__))}/../../../db/atomic_service/{atom_service._base_info.get_name()}/{atom_service._base_info.get_name()}.json",
    #     #     "w",
    #     # ) as file:
    #     #     json.dump(json_info, file, indent=4)
    #     # print(root_json_dict)
    #     # 将解析前的原文件再次导入到框架内
    #     AtomServiceUtil._loadHpp(atom_service, file_name)

    #     return atom_service
