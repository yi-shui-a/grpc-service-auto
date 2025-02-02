import re
import json

def parse_structs_from_header(header_path):
    structs = {}

    # 正则表达式来匹配结构体定义
    struct_pattern = re.compile(
        r'typedef\s+struct\s+(\w+)\s*{[^{}]*'
        r'(?:\s*(\w+)\s+([\w\s,]*)\s*;\s*)*'
        r'}\s+(\w+)\s*;',
        re.DOTALL | re.MULTILINE
    )
    print("struct_pattern".format(struct_pattern))

    with open(header_path, 'r') as file:
        content = file.read()

        # 查找所有结构体定义
        matches = struct_pattern.findall(content)
        for match in matches:
            struct_name = match[0]
            fields = []
            for field in match[1:]:
                if field.strip():
                    fields.append(field.strip())

            if fields:
                structs[struct_name] = fields

    return structs

def generate_json(structs):
    print("structs{}".format(structs))
    messages = []
    for struct_name, fields in structs.items():
        # 获取结构体标签
        label = "request" if "_Request_" in struct_name else "reply"
        message = {
            "label": label,
            "name": struct_name,
            "fields": []
        }

        id_counter = 1
        for field in fields:
            field_info = field.split()
            field_name = field_info[-1]
            field_type = " ".join(field_info[:-1])

            # 处理类型
            field_entry = {
                "name": field_name,
                "type": field_type,
                "id": id_counter,
                "chinese_name": f"输入参数{id_counter}" if "Request" in struct_name else f"输出参数{id_counter}"
            }

            if "std::vector" in field_type:
                field_entry["repeated"] = True
                field_entry["type"] = field_type.replace("std::vector<", "").replace(">", "")

            if "std::map" in field_type:
                field_entry["map"] = True
                map_info = field_type.replace("std::map<", "").replace(">", "").split(",")
                field_entry["key"] = map_info[0].strip()
                field_entry["value"] = map_info[1].strip()
                del field_entry["type"]

            message["fields"].append(field_entry)
            id_counter += 1

        messages.append(message)

    return {"messages": messages}

def write_to_json(data, output_path):
    with open(output_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

if __name__ == "__main__":
    header_path = 'sj.h'  # 替换为你的头文件路径
    output_path = 'sj.json'         # 输出的JSON文件路径

    structs = parse_structs_from_header(header_path)
    json_data = generate_json(structs)
    write_to_json(json_data, output_path)
