import json

def generate_struct_declaration(struct_name, members):
    members_str = '\n    '.join(
        f"{' ' if member['req'] else 'unsigned '} {member['type']} {member['key']}[{member['array']}];" if member.get(
            'array') else f"{' ' if member['req'] else 'unsigned '} {member['type']} {member['key']};" for member in
        members)
    return f"typedef struct {{\n    {members_str}\n}} {struct_name};\n"


def generate_c_files(json_data):
    name = json_data["name"]
    func_name = json_data["func"]
    input_struct_name = json_data["input"]["struct"]["name"]
    input_members = json_data["input"]["struct"]["member"]
    output_struct_name = json_data["output"]["struct"]["name"]
    output_members = json_data["output"]["struct"]["member"]

    header_content = f"#ifndef _{name.upper()}_H_\n#define _{name.upper()}_H_\n\n"
    header_content += generate_struct_declaration(input_struct_name, input_members)
    header_content += generate_struct_declaration(output_struct_name, output_members)

    header_content += f"\nvoid {func_name}({input_struct_name} *input, {output_struct_name} *output);\n"

    header_content += f"\n#endif // _{name.upper()}_H_\n"

    source_content = f"#include \"{name}.h\"\n\n"

    source_content += f"void {func_name}({input_struct_name} *input, {output_struct_name} *output) {{\n    // Function implementation TODO \n}}\n"

    with open(f"{name}.h", "w") as header_file:
        header_file.write(header_content)

    with open(f"{name}.c", "w") as source_file:
        source_file.write(source_content)

    print(f"C files {name}.h and {name}.c generated successfully.")


if __name__ == "__main__":
    with open(".json", "r") as json_file:
        json_data = json.load(json_file)
    generate_c_files(json_data)

