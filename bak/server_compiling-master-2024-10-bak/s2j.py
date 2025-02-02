import re

def extract_structs_and_fields_from_header(file_path):
    # 正则表达式来匹配带有typedef的struct定义
    typedef_struct_pattern = re.compile(
        r'(?:^|\n)\s*typedef\s+struct\s+\{([\s\S]*?)\}\s+([a-zA-Z_][a-zA-Z0-9_]*);',
        re.MULTILINE | re.DOTALL
    )
    
    # 正则表达式用于匹配字段定义
    field_pattern = re.compile(
        r'\s*(.*?)(\s+)([a-zA-Z_][a-zA-Z0-9_]*);'
    )

    # 读取文件
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # 查找所有匹配项
    typedef_structs = typedef_struct_pattern.findall(content)

    # 结构化输出结果
    typedef_struct_definitions = []
    for fields, name in typedef_structs:
        # 匹配字段定义
        fields_info = field_pattern.findall(fields)
        typedef_struct_definitions.append({
            'name': name,
            'fields': [
                {
                    'type': field_type.strip(),
                    'name': field_name.strip()
                }
                for field_type, _, field_name in fields_info
            ]
        })

    return typedef_struct_definitions

# 使用函数
file_path = 'atom_service_mbsb.h'  # 替换为你的文件路径
typedef_struct_definitions = extract_structs_and_fields_from_header(file_path)

# 输出结果
for typedef_struct in typedef_struct_definitions:
    print(f"Typedef Struct Name: {typedef_struct['name']}")
    print("Fields:")
    for field in typedef_struct['fields']:
        print(f"  Type: {field['type']}, Name: {field['name']}")
    print("\n")