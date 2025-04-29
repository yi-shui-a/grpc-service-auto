"""
cpp中的类型和protobuffer中类型的对应关系
"""

cpp_proto_dict = {
    "int": "int32",
    "uint": "uint32",
    "int32_t": "int32",
    "uint8_t": "int32",
    "uint16_t": "int32",
    "int8_t": "int32",
    "int16_t": "int32",
}


"""
用户输入的原task的添加后缀
"""
service_task_suffix = "_func"


"""
用户输入doc，可能出现词语拼写错误，需要纠正
"""
doc_types_correct_dict = {
    "atomic_service_name": "name",
    "file": "name",
    "date": "build_time",
    "priority": "priority_level",
}


"""
用户输入doc，必须需要的字段。如果用户没有输入，使用下面的默认值
"""
doc_types_dict = {
    "name": "",
    "chinese_name": "",
    "description": "",
    "version": "",
    "build_time": "",
    "priority_level": -999,
    "license": "",
    "service_path": "",
    "owner": {
        "maintainer": {"name": "", "email": ""},
        "developer": {
            "name": "",
            "email": "",
        },
    },
    "resource_requirement": {},
    "operating_system": [
        {
            "os_name": "",
            "os_version": {},
        }
    ],
}


"""
cpp中的类型和idl中类型的对应关系

idl支持的数据类型

"""
cpp_idl_dict = {
    "uint8": "octet",
    "int": "long",
    "uint": "unsigned long",
    "int32_t": "long",
    "uint8_t": "octet",
    "uint16_t": "unsigned short",
    "int16_t": "short",
    "int32": "long",
}
