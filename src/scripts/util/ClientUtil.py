import sys
import os
import re
from jinja2 import Template
import subprocess
from typing import List, Dict
import json

from .Util import Util
from .AtomServiceUtil import AtomServiceUtil
from ..entity import Client, Message
from ..config import (
    cpp_proto_dict,
    cpp_idl_dict,
)


class ClientUtil:

    async_client_suffix = "_async_client"
    sync_client_suffix = "_sync_client"

    def __init__(self, client):
        pass

    @staticmethod
    def accomplishAllClient(orchestrattion_info: dict):
        """
        完成所有客户端的所有流程
        """
        client: Client = ClientUtil.generateSyncClient(orchestrattion_info)
        client_path: str = (
            f"{os.path.dirname(os.path.abspath(__file__))}/../../../db/client/{client.get_name()}/"
        )
        # 生成通信模块代码
        Util.generateHeaderHppAndCpp(client_path + "sync_client/")

        ClientUtil.generateSyncClientCMakeLists(client)
        ClientUtil.compileSyncClient(client)

    @staticmethod
    def generateSyncClientCMakeLists(client: Client):
        client_template = Template(
            open(
                f"{os.path.dirname(os.path.abspath(__file__))}/../../templates/sync_server_client_process_template/sync_client_compile_cmake_template.j2"
            ).read()
        )

        res_str = client_template.render(
            project_name=client.get_name() + ClientUtil.sync_client_suffix,
            services=client._services,
            idl_list=client._dds_topic,
        )

        # 确保目录存在
        os.makedirs(
            f"{os.path.dirname(os.path.abspath(__file__))}/../../../db/client/{client.get_name()}/sync_client/",
            exist_ok=True,
        )

        # 将res_str写入框架内的cpp文件中，同名不同路径
        with open(
            f"{os.path.dirname(os.path.abspath(__file__))}/../../../db/client/{client.get_name()}/sync_client/CMakeLists.txt",
            "w",
        ) as file:
            file.write(res_str)
        print(
            f"{os.path.dirname(os.path.abspath(__file__))}/../../../db/client/{client.get_name()}/sync_client/CMakeLists.txt generated successfully!"
        )

    @staticmethod
    def compileSyncClient(client: Client):
        client_dir = f"{os.path.dirname(os.path.abspath(__file__))}/../../../db/client/{client.get_name()}/sync_client/"

        Util.compileCmakeProject(
            client_dir,
            client.get_name() + ClientUtil.sync_client_suffix,
            file_type="cpp",
        )

    @staticmethod
    def generateSyncClient(orchestrattion_info: dict) -> Client:
        """
        client头部模版生成


        目前假设：
        1. 开始节点转发的idl只有基本类型而且只有一个结构体
        2. dds数据结构在开始node的dataBind的idl中
        """
        # TODO: 通过json生成client
        # 获取出现的service列表（出现多次只记录一次）
        # 定义idl的目录 idl_path + idl名称（module）
        # idl_path: str = (
        #     f"{os.path.dirname(os.path.abspath(__file__))}/../../../db/client/{orchestrattion_info.get('name', '')}/idl"
        # )
        # 解析并编译开始节点中的结构体为proto文件
        ClientUtil._compileStartStruct(orchestrattion_info)
        idl_list: List[str] = list()

        # 定义输出字符串
        output_str: str = ""

        service_list: List[str] = list()
        for node in orchestrattion_info.get("nodes", []):
            if (
                node.get("type", "") == "SERVICE"
                and node.get("title", "") not in service_list
            ):
                service_list.append(node.get("title", ""))
        # 为orchestrattion_info的node添加服务的具体信息，即添加一个service_info属性
        for node in orchestrattion_info.get("nodes", []):
            if node.get("type", "") == "SERVICE":
                node["service_info"] = AtomServiceUtil.getAtomServiceJson(
                    node.get("title", "")
                )
            if node.get("type", "") == "START":
                node["message_info"] = ClientUtil._getIdlJson(
                    orchestrattion_info.get("name", ""), node.get("module", "")
                )

        # 加载 “开始” 中的输出数据
        #  “开始” 节点列表
        start_node_list: list[dict] = list()
        for node in orchestrattion_info.get("nodes", []):
            if node.get("type", "") == "START":
                start_node_list.append(node)
                # 将module名称加入idl_list
                idl_list.append(node.get("module", ""))
        # “开始” 节点的连接列表,Dict[id, List[str]]
        nodeId_connection_dict: Dict[str, List[dict]] = dict()
        for start_node in start_node_list:
            start_connection_list: list[dict] = list()
            for connection in orchestrattion_info.get("connections", []):
                if connection.get("source", "") == start_node.get("id", ""):
                    start_connection_list.append(connection)
            nodeId_connection_dict[start_node.get("id", "")] = start_connection_list
        print(json.dumps(nodeId_connection_dict, indent=4))

        # 定义声明对象的列表
        declare_list: List[list] = list()
        for node in orchestrattion_info.get("nodes", []):
            if node.get("type", "") == "SERVICE":
                temp_list: list = list()
                temp_list.append(
                    ClientUtil._getRequestMessage(node, node.get("method", "")).get(
                        "name", ""
                    )
                )
                temp_list.append(node.get("id", ""))
                declare_list.append(temp_list)

        # 定义赋值关系
        assignment_list: List[list] = list()

        for start_node in start_node_list:
            # 遍历连接列表，获取连接的目标节点的id
            connection_list: list[dict] = nodeId_connection_dict.get(
                start_node.get("id", ""), []
            )
            for connection in connection_list:
                target_node_id = connection.get("target", "")
                # 获取目标节点的信息
                target_node = ClientUtil._getNode(orchestrattion_info, target_node_id)
                target_message = ClientUtil._getRequestMessage(
                    target_node, target_node.get("method", "")
                )
                # 最多考虑一层嵌套
                for field in target_message.get("fields", []):
                    if ClientUtil.isStruct(target_node, field) == dict():
                        temp_list = list()
                        temp_list.append(target_node.get("id", ""))
                        temp_list.append(field.get("name", ""))
                        temp_list.append(start_node.get("id", ""))
                        temp_list.append(field.get("name", ""))
                        assignment_list.append(temp_list)
                    else:
                        nest_list: list = list()
                        for inner_field in ClientUtil.isStruct(target_node, field):
                            nest_list.append(inner_field.get("name", ""))
                            temp_list = list()
                            temp_list.append(target_node.get("id", ""))
                            temp_list.append(
                                ".".join(nest_list) + "." + inner_field.get("name", "")
                            )
                            temp_list.append(start_node.get("id", ""))
                            temp_list.append(
                                ".".join(nest_list) + "." + inner_field.get("name", "")
                            )
                            assignment_list.append(temp_list)

        # 加载client_header模版
        client_header_template = Template(
            open(
                f"{os.path.dirname(os.path.abspath(__file__))}/../../templates/sync_server_client_process_template/sync_client_header_template.j2"
            ).read()
        )
        client_header_str = client_header_template.render(
            orchestrattion_info=orchestrattion_info,
            service_list=service_list,
            idl_list=idl_list,
            start_node_list=start_node_list,
            assignment_list=assignment_list,
            declare_list=declare_list,
        )

        # 将 client_header 的字符串添加到 output_str
        output_str = output_str + client_header_str

        # 运行阶段
        """
        client中部模版生成
        
        
        如果一个节点已经运行添加字段used = true
        为每个节点添加一个prev_id_list属性，标记前置节点数量
        为每个节点添加一个assign_num属性，标记当前节点的赋值数量,只有等于len(prev_id_list)时，才可以运行
        """
        # 创建上面三个属性并赋初值
        for node in orchestrattion_info.get("nodes", []):
            if node.get("type", "") != "START":
                node["used"] = False
                node["prev_id_list"] = list()
                node["assign_num"] = 0
                for connection in orchestrattion_info.get("connections", []):
                    if connection.get("target", "") == node.get("id", ""):
                        node["prev_id_list"].append(connection.get("source", ""))

        # 找到开始节点后可以运行的节点
        for node in orchestrattion_info.get("nodes", []):
            if node.get("type", "") == "START":
                for connection in orchestrattion_info.get("connections", []):
                    if connection.get("source", "") == node.get("id", ""):
                        # 将该节点的assign_num加1
                        target_node = ClientUtil._getNode(
                            orchestrattion_info, connection.get("target", "")
                        )
                        target_node["assign_num"] += 1

        # end节点的列表
        end_node_list: List[dict] = list()
        for node in orchestrattion_info.get("nodes", []):
            if node.get("type", "") == "END":
                end_node_list.append(node)

        # 保存指向end节点的node
        end_prev_node_list: list[dict] = list()
        for connection in orchestrattion_info.get("connections", []):
            if connection.get("target", "") in [
                end_node.get("id", "") for end_node in end_node_list
            ]:
                end_prev_node_list.append(
                    ClientUtil._getNode(
                        orchestrattion_info, connection.get("source", "")
                    )
                )

        # 标志位，表明是否结束
        end_flag = False
        while not end_flag:
            # 如果一个节点的运算已经完成，添加一个node属性为uesd = true，否则该属性为空
            # available_list存储当前可以执行的节点, call_template_list存储当前可以执行的节点的模版需要字段的列表
            available_list: List[dict] = list()
            call_template_list: List[str] = list()
            for node in orchestrattion_info.get("nodes", []):
                if (
                    node.get("type", "") != "START"
                    and node["assign_num"] == len(node["prev_id_list"])
                    and node["used"] == False
                ):
                    available_list.append(node)
                    node["used"] = True
                    temp_call_template: list = list()
                    temp_call_template.append(
                        ClientUtil._getResponseMessage(node, node["method"]).get(
                            "name", ""
                        )
                    )
                    temp_call_template.append(node.get("id", ""))
                    temp_call_template.append(node.get("title", ""))
                    temp_call_template.append(node.get("method", ""))
                    temp_call_template.append(node.get("id", ""))
                    call_template_list.append(temp_call_template)

            # # 将当前获取的值传给下一个节点
            # # 获取当前运算完的节点和下一级节点的连线和node列表
            # next_connection_list: List[dict] = list()
            # next_node_list: List[dict] = list()
            # # 遍历连线，获取下一级节点的信息
            # for connection in orchestrattion_info.get("connections", []):
            #     if connection.get("source", "") in [
            #         node.get("id", "") for node in available_list
            #     ]:
            #         next_connection_list.append(connection)
            # # 遍历下一级节点的信息，获取下一级节点的信息
            # for node in orchestrattion_info.get("nodes", []):
            #     if node.get("id", "") in [
            #         connection.get("target", "") for connection in next_connection_list
            #     ]:
            #         next_node_list.append(node)

            # 定义赋值关系
            assignment_list: List[list] = list()

            # 遍历所有available节点，将available节点的输出数据传给下一级节点
            for prev_node in available_list:
                # 找到以prev_node 开始的所有连线
                connection_list: list[dict] = list()
                for connection in orchestrattion_info.get("connections", []):
                    if connection.get("source", "") == prev_node.get("id", ""):
                        # 将该节点的assign_num(赋值次数)加1
                        ClientUtil._getNode(
                            orchestrattion_info, connection.get("target", "")
                        )["assign_num"] += 1
                        # 如果下一级节点是end节点，不需要添加
                        if connection.get("target", "") in [
                            end_node.get("id", "") for end_node in end_node_list
                        ]:
                            continue
                        connection_list.append(connection)
                # 遍历所有连线，将连线的目标节点的输入数据赋值给下一级节点, 只考虑一层嵌套
                for connection in connection_list:
                    target_node_id = connection.get("target", "")
                    # 获取目标节点的信息
                    target_node = ClientUtil._getNode(
                        orchestrattion_info, target_node_id
                    )
                    target_message = ClientUtil._getRequestMessage(
                        target_node, target_node.get("method", "")
                    )
                    # 最多考虑一层嵌套
                    for field in target_message.get("fields", []):
                        if ClientUtil.isStruct(target_node, field) == dict():
                            temp_list = list()
                            temp_list.append(target_node.get("id", ""))
                            temp_list.append(field.get("name", ""))
                            temp_list.append(prev_node.get("id", ""))
                            temp_list.append(field.get("name", ""))
                            assignment_list.append(temp_list)
                        else:
                            nest_list: list = list()
                            for inner_field in ClientUtil.isStruct(target_node, field):
                                nest_list.append(inner_field.get("name", ""))
                                temp_list = list()
                                temp_list.append(target_node.get("id", ""))
                                temp_list.append(
                                    ".".join(nest_list)
                                    + "."
                                    + inner_field.get("name", "")
                                )
                                temp_list.append(prev_node.get("id", ""))
                                temp_list.append(
                                    ".".join(nest_list)
                                    + "."
                                    + inner_field.get("name", "")
                                )
                                assignment_list.append(temp_list)

            # 写入输出字符串
            client_content_template = Template(
                open(
                    f"{os.path.dirname(os.path.abspath(__file__))}/../../templates/sync_server_client_process_template/sync_client_content_template.j2"
                ).read()
            )
            client_content_str = client_content_template.render(
                call_template_list=call_template_list,
                assignment_list=assignment_list,
            )
            output_str = output_str + client_content_str
            # 判断循环是否应该结束,所有end节点的 assign_num都大于等于len(prev_id_list)，结束循环
            if all(
                node["assign_num"] >= len(node["prev_id_list"])
                for node in end_node_list
            ):
                end_flag = True

        """
        client尾部模版生成
        
        
        构造client的尾部字符串
        """
        # 定义赋值关系
        assignment_list: List[list] = list()
        # 打印输出字符串
        for prev_end_node in end_prev_node_list:
            messgae: dict = ClientUtil._getResponseMessage(
                prev_end_node, prev_end_node.get("method", "")
            )
            # 最多考虑一层嵌套
            for field in messgae.get("fields", []):
                if ClientUtil.isStruct(prev_end_node, field) == dict():
                    temp_list = list()
                    temp_list.append(prev_end_node.get("id", ""))
                    temp_list.append(field.get("name", ""))
                    assignment_list.append(temp_list)
                else:
                    nest_list: list = list()
                    for inner_field in ClientUtil.isStruct(target_node, field):
                        nest_list.append(inner_field.get("name", ""))
                        temp_list = list()
                        temp_list.append(prev_end_node.get("id", ""))
                        temp_list.append(
                            ".".join(nest_list) + "." + inner_field.get("name", "")
                        )
                        assignment_list.append(temp_list)

        # 加载client_footer模版
        client_footer_template = Template(
            open(
                f"{os.path.dirname(os.path.abspath(__file__))}/../../templates/sync_server_client_process_template/sync_client_footer_template.j2"
            ).read()
        )
        client_footer_str = client_footer_template.render(
            orchestrattion_info=orchestrattion_info,
            service_list=service_list,
            assignment_list=assignment_list,
            start_node_list=start_node_list,
        )
        output_str = output_str + client_footer_str

        """
        保存文件到client目录
        """
        os.makedirs(
            f"{os.path.dirname(os.path.abspath(__file__))}/../../../db/client/{orchestrattion_info.get('name', '')}/sync_client/",
            exist_ok=True,
        )
        client_file = f"{os.path.dirname(os.path.abspath(__file__))}/../../../db/client/{orchestrattion_info.get('name', '')}/sync_client/{orchestrattion_info.get('name', '')}.cpp"
        with open(client_file, "w", encoding="utf-8") as f:
            f.write(output_str)
        # 输出字符串
        print("SUCCESS: generated " + client_file)

        """
        构建并返回一个client对象
        """
        res_client = Client()
        res_client.set_name(orchestrattion_info.get("name", ""))
        print("client: " + res_client.get_name())
        # 这里将module的内容作为topic导入，未来需要将client中的topic改为module
        for start_node in start_node_list:
            res_client.add_dds_topic(start_node.get("module", ""))
        for service_name in service_list:
            res_client.add_service(service_name)
        return res_client

    # 解析并编译开始节点中的结构体为proto文件
    @staticmethod
    def _compileStartStruct(orchestrattion_info: dict) -> str:
        """
        保存准备
        """
        # 确保idl目录存在
        idl_path: str = (
            f"{os.path.dirname(os.path.abspath(__file__))}/../../../db/client/{orchestrattion_info.get('name', '')}/idl"
        )
        os.makedirs(
            idl_path,
            exist_ok=True,
        )

        """
        解析json
        """
        # 找到开始节点
        start_node_list: list[dict] = list()
        for node in orchestrattion_info.get("nodes", []):
            if node.get("type", "") == "START":
                start_node_list.append(node)
        # 解析开始节点的结构体为一个message
        start_node_messages_list: list[dict] = list()
        for start_node in start_node_list:
            # 输入字符串
            input_str: str = start_node.get("struct", "")

            messages = list()
            # 正则匹配结构体定义（支持多行和单行）
            message_info_pattern = re.compile(
                r"typedef\s+struct\s*{([^}]*)}[^{}]*?(\w+);",  # 匹配结构体定义
                re.DOTALL,  # 使 . 匹配换行符
            )

            # 匹配所有结构体
            message_info_matches = message_info_pattern.finditer(input_str)
            for match in message_info_matches:
                fields_text = match.group(1).strip()  # 字段定义部分
                struct_name = match.group(2).strip()  # 结构体名称
                # 解析字段
                fields = []
                field_id = 1
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

                messages.append(
                    {"name": struct_name, "description": "", "fields": fields}
                )
            # 保存到json到idl中，命名为start节点id
            # 保存到idl文件夹
            os.makedirs(
                f"{idl_path}/{start_node.get('module', '')}",
                exist_ok=True,
            )
            with open(
                f"{idl_path}/{start_node.get('module', '')}/{start_node.get('module', '')}.json",
                "w",
                encoding="utf-8",
            ) as f:
                f.write(
                    json.dumps(
                        {"module": start_node["module"], "messages": messages}, indent=4
                    )
                )

            start_node_messages_list.append(messages)

        # 遍历start_node_messages_list，生成idl文件
        for i in range(len(start_node_messages_list)):
            # for start_node_messages in start_node_messages_list:
            module_name = start_node_list[i].get("module", "")
            # 遍历message，生成idl文件
            idl_template = Template(
                open(
                    f"{os.path.dirname(os.path.abspath(__file__))}/../../templates/dds_process_template/idl_template.j2"
                ).read()
            )
            # 构建message列表
            messages: Message = list()
            for message in start_node_messages_list[i]:
                temp = Message()
                temp.set_info(message)
                messages.append(temp)
            ClientUtil.__type_convert(messages=messages)
            res_str = idl_template.render(
                module_name=start_node_list[i].get("module", ""),
                messages=messages,
            )

            with open(
                f"{idl_path}/{module_name}/{module_name}.idl",
                "w",
                encoding="utf-8",
            ) as f:
                f.write(res_str)

            # 生成CMakeLists.txt
            cmake_template = Template(
                open(
                    f"{os.path.dirname(os.path.abspath(__file__))}/../../templates/dds_process_template/idl_compile_cmake_template.j2"
                ).read()
            )
            res_str = cmake_template.render(
                project_name=module_name,
            )
            # 保存到idl文件夹
            with open(
                f"{idl_path}/{module_name}/CMakeLists.txt",
                "w",
                encoding="utf-8",
            ) as f:
                f.write(res_str)

            # 编译idl文件
            Util.compileCmakeProject(
                f"{idl_path}/{start_node.get('module', '')}/",
                module_name,
                file_type="idl",
            )

    @staticmethod
    def _getServiceName(orchestrattion_info: dict, id: str) -> str:
        for node in orchestrattion_info.get("nodes", []):
            if node.get("id", "") == id:
                return node.get("title", "")

    @staticmethod
    def _getNode(orchestrattion_info: dict, id: str) -> dict:
        for node in orchestrattion_info.get("nodes", []):
            if node.get("id", "") == id:
                return node

    # 根据message_name获取message的dict
    @staticmethod
    def _getMessage(target_node: dict, message_name: str) -> dict:
        for message in target_node.get("service_info", []).get("messages", []):
            if message.get("name", "") == message_name:
                return message

    # 根据method_name获取request的message
    @staticmethod
    def _getRequestMessage(target_node: dict, method_name: str) -> dict:
        request_message = ""
        for method in target_node.get("service_info", []).get("methods", []):
            if method.get("name", "") == method_name:
                request_message = method.get("requestMsg", "")
        for message in target_node.get("service_info", []).get("messages", []):
            if message.get("name", "") == request_message:
                return message

    # 根据method_name获取response的message
    @staticmethod
    def _getResponseMessage(target_node: dict, method_name: str) -> dict:
        response_message = ""
        for method in target_node.get("service_info", []).get("methods", []):
            if method.get("name", "") == method_name:
                response_message = method.get("responseMsg", "")
        for message in target_node.get("service_info", []).get("messages", []):
            if message.get("name", "") == response_message:
                return message

    # 判断该字段是否是一个结构体，如果是，返回结构体，否则返回空dict
    @staticmethod
    def isStruct(target_node: dict, field: dict) -> dict:
        for message in target_node.get("service_info", []).get("messages", []):
            if message.get("name", "") == field.get("name", ""):
                return message
        return dict()

    @staticmethod
    def getSourceNodeNum(orchestrattion_info: dict, id: str) -> int:
        num: int = 0
        for connection in orchestrattion_info.get("connections", []):
            if connection.get("target", "") == id:
                num += 1
        return num

    @staticmethod
    def _getIdlJson(client_name: str, struct_name: str) -> dict:
        # 打开idl的json文件
        idl_file = f"{os.path.dirname(os.path.abspath(__file__))}/../../../db/client/{client_name}/idl/{struct_name}/{struct_name}.json"
        with open(idl_file, "r", encoding="utf-8") as f:
            idl_json = json.load(f)
            return idl_json
        return dict()

    @staticmethod
    def __type_convert(messages: List[Message]):
        # 修改数据类型
        # 删除std::
        for message in messages:
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
