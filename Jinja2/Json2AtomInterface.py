#!/root/venv/bin/python

import os
import json
import sys

def generate_atom_files(data, out_cpp_path, out_h_path):
    try:
        with open(data, 'r') as json_file:
            json_data = json.load(json_file)

    except json.JSONDecodeError as err:
        print(f"JSONDecodeError: {err}")
        return []

    # # Generate service_number and atom_name
    # atom_names = []
    # server = data.get('server', '')
    # server_name = server['name']
    # print("server_name:",server_name)
    # for service in data.get('service', []):  # use .get() avoid KeyError
    #     atom_names.append(service['name'])
    # print("atom_names:",atom_names)

    name = json_data['implement_rpc']["atom_name"]
    header_content = f"#ifndef _{name.upper()}_H_\n#define _{name.upper()}_H_\n\n"
    # include <****>
    header_content += f"#include <grpcpp/grpcpp.h>\n#include <string>\n#include <vector>\n"
    header_content += f"#include <map>\n"

    # name = json_data["atom_name"]
    func_name = json_data['implement_rpc']["atom_interface"]

    for message in json_data["messages"]:
        if message["lable"] == "request":
            header_content += f"//Request\ntypedef struct {message['name']}_struct {{\n"
            for field in message["fields"]:
                if field["type"] == "string":
                    header_content += f"    std::string {field['name']};\n"
                elif 'repeated' in field:
                    if field["type"] == "string":
                        header_content += f"    std::vector<std::string> {field['name']};\n"
                    elif field["type"] == "int32":
                        header_content += f"    std::vector<int32_t> {field['name']};\n"
                    elif field["type"] == "int64":
                        header_content += f"    std::vector<int64_t> {field['name']};\n"
                    elif field["type"] == "bool":
                        header_content += f"    std::vector<bool> {field['name']};\n"
                    elif field["type"] == "double":
                        header_content += f"    std::vector<double> {field['name']};\n"
                    elif field["type"] == "float":
                        header_content += f"    std::vector<float> {field['name']};\n"
                    elif field["type"] == "bytes":
                        header_content += f"    std::vector<uint8_t> {field['name']};\n"
                    elif field["type"] == "uint32":
                        header_content += f"    std::vector<uint32_t> {field['name']};\n"
                    elif field["type"] == "uint64":
                        header_content += f"    std::vector<uint64_t> {field['name']};\n"
                    elif field["type"] == "sint32":
                        header_content += f"    std::vector<int32_t> {field['name']};\n"
                    else:
                        print(">>>> request Unknown type: ", field["type"])
                        # header_content += f"std::vector<{field["type"]}> {field['name']};\n"
                    # header_content += f"    int32_t {field['name']};\n"
                elif field["type"] == "int32":
                        header_content += f"    int32_t {field['name']};\n"
                elif 'map' in field:
                    if field['key'] == 'int32' and field['value'] == 'int32':
                        header_content += f"    std::map<std::int32_t, std::int32_t> {field['name']};\n"
                    elif field['key'] == 'int32' and field['value'] != 'int32':
                        header_content += f"    std::{field['type']}<std::int32_t, std::{field['value']}> {field['name']};\n"
                    elif field['key'] != 'int32' and field['value'] == 'int32':
                        header_content += f"    std::{field['type']}<std::{field['key']}, std::int32_t> {field['name']};\n"
                    else:
                        header_content += f"    std::{field['type']}<std::{field['key']}, std::{field['value']}> {field['name']};\n"
                    # header_content +=  f"    std::{field['type']}<std::{field['key']}, std::{field['value']}> {field['name']};\n"
                else:
                    header_content += f"    {field['type']} {field['name']};\n"
            header_content += f"}} {message['name']}_st;\n"
            request_struct_name = message['name']+"_st"
            
        elif message["lable"] == "reply":
            header_content += f"//Reply\ntypedef struct {message['name']}_struct{{\n"
            for field in message["fields"]:
                if field["type"] == "string":
                    header_content += f"    std::string {field['name']};\n"
                elif 'repeated' in field:        
                    if field["type"] == "string":
                        header_content += f"    std::vector<std::string> {field['name']};\n"
                    elif field["type"] == "int32":
                        header_content += f"    std::vector<int32_t> {field['name']};\n"
                    elif field["type"] == "int64":
                        header_content += f"    std::vector<int64_t> {field['name']};\n"
                    elif field["type"] == "bool":
                        header_content += f"    std::vector<bool> {field['name']};\n"
                    elif field["type"] == "double":
                        header_content += f"    std::vector<double> {field['name']};\n"
                    elif field["type"] == "float":
                        header_content += f"    std::vector<float> {field['name']};\n"
                    elif field["type"] == "bytes":
                        header_content += f"    std::vector<uint8_t> {field['name']};\n"
                    elif field["type"] == "uint32":
                        header_content += f"    std::vector<uint32_t> {field['name']};\n"
                    elif field["type"] == "uint64":
                        header_content += f"    std::vector<uint64_t> {field['name']};\n"
                    elif field["type"] == "sint32":
                        header_content += f"    std::vector<int32_t> {field['name']};\n"
                    else:
                        print(">>>> request Unknown type: ", field["type"])
                        # header_content += f"std::vector<{field["type"]}> {field['name']};\n"
                    # header_content += f"    int32_t {field['name']};\n"
                elif field["type"] == "int32":
                        header_content += f"    int32_t {field['name']};\n"
                elif 'map' in field:
                    if field['key'] == 'int32' and field['value'] == 'int32':
                        header_content += f"    std::map<std::int32_t, std::int32_t> {field['name']};\n"
                    elif field['key'] == 'int32' and field['value'] !=  'int32':
                        header_content += f"    std::{field['type']}<std::int32_t, std::{field['value']}> {field['name']};\n"
                    elif field['key'] != 'int32' and field['value'] == 'int32':
                        header_content += f"    std::{field['type']}<std::{field['key']}, std::int32_t> {field['name']};\n"
                    else:
                        header_content += f"    std::{field['type']}<std::{field['key']}, std::{field['value']}> {field['name']};\n"
                    # header_content +=  f"    std::{field['type']}<std::{field['key']}, std::{field['value']}> {field['name']};\n"
                else:
                    header_content += f"    {field['type']} {field['name']};\n"
            header_content += f"}} {message['name']}_st;\n"
            reply_struct_name = message['name'] + "_st"

    header_content += f"\nvoid {func_name}({request_struct_name} *request, {reply_struct_name} *reply);\n"

    header_content += f"\n#endif // _{name.upper()}_H_\n"

    source_content = f"#include \"../atom_inc/{name}.h\"\n\n"
    #  TODO: Add implementation

    source_content += f"void {func_name}({request_struct_name} *request, {reply_struct_name} *reply) {{\n    // Function implementation TODO \n}}\n"

    #  TODO: Add implementation

    # with open(f"{out_cpp_path}/{name}.cpp", "w") as source_file:
    #     source_file.write(source_content)

    with open(f"{out_h_path}/{name}.h", "w") as header_file:
        header_file.write(header_content)

    print(f"|- {name}.cpp and {name}.h generated successfully.")

def open_json_file(json_file):
    try:
        with open(json_file, 'r') as json_file:
            json_data = json.load(json_file)
        return json_data
    except json.JSONDecodeError as err:
        print(f"JSONDecodeError: {err}")
        return []

if __name__ == "__main__":
    out_cpp_path = "../atom_src"
    out_h_path = "../atom_inc"
    # generate_atom_files("../Json/example.json", out_cpp_path ,out_h_path)

    json_data = open_json_file("../Json/config_atom_name.json") 
    atom_list = json_data['implement_rpc']["atom_name"]
    for i, atom_json_name in enumerate(atom_list):
        atom_file_path = "../Json/" + atom_json_name + ".json"
        print("| -{} {}".format(i, atom_json_name))
        generate_atom_files(atom_file_path, out_cpp_path, out_h_path)