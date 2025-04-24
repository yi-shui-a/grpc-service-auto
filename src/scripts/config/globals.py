cpp_types = {
    "int": "int32",
    "uint": "uint32",
    "int32_t": "int32",
    "uint8_t": "int32",
    "uint16_t": "int32",
    "int8_t": "int32",
    "int16_t": "int32",
}

service_task_suffix = "_func"

doc_types_correct_dict = {
    "atomic_service_name": "name",
    "file": "name",
    "date": "build_time",
    "priority": "priority_level",
}

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
