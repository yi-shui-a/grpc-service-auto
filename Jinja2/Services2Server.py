#!/root/venv/bin/python
import os
import sys
import jinja2
import json
from jinja2 import Template, FileSystemLoader, Environment

# personalized template
import extract_json_info
import Json2proto
import Json2AtomInterface

# # get current dir
current_dir = os.path.dirname(os.path.abspath(__file__))
# print("current_dir: ", current_dir)
# # get parent dir
parent_dir = os.path.dirname(current_dir)
# print("parent_dir: ", parent_dir)
# # get grandparent dir
# grandparent_dir = os.path.dirname(parent_dir)

# step0: Depend on ../Jinja2/ServerBaseInfo.json --> parse service number and service name
# def parse_ServerBaseInfo_json(file_path_name):
#     with open(file_path_name, 'r') as json_file:
#         data = json.load(json_file)
#     # Generate service_number and service_name
#     service_names = []
#     for service in data['service']:
#         # service_names.append(service['name'])
#         print(service_names)
#     print(service_names)
#     return service_names

def parse_ServerBaseInfo_json(file_path_name):
    try:
        with open(file_path_name, 'r') as json_file:
            data = json.load(json_file)
    except json.JSONDecodeError as err:
        print(f"JSONDecodeError: {err}")
        return []
    # Generate service_number and service_name
    service_names = []
    server = data.get('server', '')
    server_name = server['name']
    print("server_name:",server_name)
    for service in data.get('service', []):  # use .get() avoid KeyError
        service_names.append(service['name'])
    print("service_names:",service_names)
    return server_name, service_names
# step1: Depend on ../Json/ atom_service_*.json -->  json file to generate proto file
def from_json_to_proto(json_input_name, proto_output_name):
    Json2proto.generate_proto_file(json_input_name, proto_output_name)
# step2: Depend on ../Json/ *.json -->  generate extracted_json file or code 
# step3: Depend on ../Json/ *_extract.json -->  generate service IMPL class template file
# step4: Depend on ../Jinja2/ Server_impl_template.j2 -->  generate service IMPL class file
def jinjaTemplate2IMPL_Class(json_input_name, class_template_output_name):
    # jinja2 template loader path
    j2_loader = FileSystemLoader('./Jinja2')
    # define env， template loader
    env = Environment(loader=j2_loader)
    # get the template file
    j2_tmpl = env.get_template('./Server_impl_template.j2')
    data = extract_json_info.extract_json2template(json_input_name)
    # set parameters to template and render it
    result = j2_tmpl.render(data)
    # print(result)
    with open(class_template_output_name, 'w') as f:
        f.write(result)
# step4: Depend on ../Jinja2/ Client_impl_template.j2 -->  generate client class file
def jinjaTemplate2Client_Class(json_input_name, class_template_output_name):
    # jinja2 template loader path
    j2_loader = FileSystemLoader('./Jinja2')
    # define env， template loader
    env = Environment(loader=j2_loader)
    # get the template file
    j2_tmpl = env.get_template('./Client_impl_template.j2')
    data = extract_json_info.extract_json2template(json_input_name)
    # set parameters to template and render it
    result = j2_tmpl.render(data)
    # print(result)
    with open(class_template_output_name, 'w') as f:
        f.write(result)
# Step5 : Depend on ../Jinja2/ *_ServerMain_template.j2 -->  generate service serverMain.cpp
def genServerMainCpp(data, class_template_output_name):
    # jinja2 template loader path
    j2_loader = FileSystemLoader('./Jinja2')
    # j2_loader = FileSystemLoader('./Jinja2')
    # define env， template loader
    env = Environment(loader=j2_loader)
    # get the template file
    j2_tmpl = env.get_template('./ServerMain_template.j2')
    # set parameters to template and render it
    result = j2_tmpl.render(data=data)
    # print(result)
    with open(class_template_output_name, 'w') as f:
        f.write(result)

def genClientMainCpp(data, class_template_output_name):
    # jinja2 template loader path
    j2_loader = FileSystemLoader('./Jinja2')
    # define env， template loader
    env = Environment(loader=j2_loader)
    # get the template file
    j2_tmpl = env.get_template('./ClientMain_template.j2')
    # set parameters to template and render it
    result = j2_tmpl.render(data=data)
    # print(result)
    with open(class_template_output_name, 'w') as f:
        f.write(result)

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> AsyncServerMain  Begain<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

def parse_ServerBaseInfo_json_async(file_path_name):
    try:
        with open(file_path_name, 'r') as json_file:
            data = json.load(json_file)
    except json.JSONDecodeError as err:
        print(f"JSONDecodeError: {err}")
        return []
    # Generate service_number and service_name
    service_names = []
    server = data.get('server', '')
    server_name = server['name']
    # print("server_name:",server_name)
    for service in data.get('service', []):  # use .get() avoid KeyError
        service_names.append(service['name'])
    # print("service_names:",service_names)
    return server_name, service_names

def extract_service_json_info_async(source_file_name):
    try:
        with open(source_file_name, 'r') as json_file:
            json_data = json.load(json_file)
    except json.JSONDecodeError as err:
        print(f"JSONDecodeError: {err}")
        return []

    # extract package info
    # package_info = {
    #     "syntax": json_data.get("syntax"),
    #     "package_name": json_data.get("package"),
    #     "service_name": json_data.get("service_name"),
    #     "request_name": json_data.get("request"),
    #     "reply_name": json_data.get("reply"),
    #     "atom_interface": json_data.get("atom_interface"),
    #     "atom_name": json_data.get("atom_name")
    # }

    package_info_modified = {
        "syntax": json_data['implement_rpc']['syntax'],
        "package_name": json_data['implement_rpc']['package'],
        "service_name": json_data['implement_rpc']['service_name'],
        "request_name": json_data['implement_rpc']['request'],
        "reply_name": json_data['implement_rpc']['reply'],
        "atom_interface": json_data['implement_rpc']['atom_interface'],
        "atom_name": json_data['implement_rpc']['atom_name'],
    }
    # extract messages list
    messages_info = json_data.get('messages', [])

    # 'lable' is a custom key that you can use to identify the messages 
    # in order to build jinja template
    messages_dict = {msg['lable']: {
        "name": msg["name"],
        "fields": [
            {"name": field["name"], "type": field["type"], "id": field["id"], 
            "repeated": field.get("repeated", False),"map": field.get("map", False)}
            for field in msg["fields"]
        ]
    } for msg in messages_info}

    # extrac services info
    services_info = {}
    for service in json_data.get("services", []):
        methods_info = []
        for method in service.get("methods", []):
            method_dict = {
                "name": method.get("name"),
                "requestType": method.get("requestType"),
                "responseType": method.get("responseType"),
            }
            methods_info.append(method_dict)
        services_info["name"] = service.get("name")
        services_info["methods"] = methods_info
    # save extracted_info to dict
    extracted_info = {
        "package": package_info_modified,
        "messages": messages_dict,
        "services": services_info
    }
    return extracted_info

def extractServerBase2AsyncTemplate():
    serverBaseJson = "./Jinja2/ServerBaseInfo.json"
    server_name, services_name = parse_ServerBaseInfo_json_async(serverBaseJson)
    source_folder = './Json'
    # extract all json info
    all_services_info = []
    for service in services_name:
        source_file_name = f'{service}.json'    
        source_file_path = os.path.join(source_folder, source_file_name)
        all_services_info.append(extract_service_json_info_async(source_file_path))

    with open("async_server_template.json", 'w') as outfile:
        json.dump(all_services_info, outfile, indent=2)
    return all_services_info

def AsyncServerTemplate2_AsyncServerMain(async_main_template_output_name):
    # jinja2 template loader path
    j2_loader = FileSystemLoader('./Jinja2')
    # define env， template loader
    env = Environment(loader=j2_loader)
    # get the template file
    j2_tmpl = env.get_template('./async_server_template.j2')
    # data = extract_json_info.extract_json2template(json_input_name)
    # set parameters to template and render it

    ## --> data = async_server_template.json
    data = extractServerBase2AsyncTemplate()

    result = j2_tmpl.render(data=data)
    # print(result)
    with open(async_main_template_output_name, 'w') as f:
        f.write(result)

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> AsyncServerMain END <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

def main(ServerBaseInfo_json_file):
    # Test Template
    server_name, services_name = parse_ServerBaseInfo_json(ServerBaseInfo_json_file)
    print(">>>> ")
    print(">>>>[INFO] Step1: parse ServerBaseInfo.json")
    # print(services_name)
    # Generate proto file
    for service_name in services_name:
        source_folder = './Json'
        target_folder = './protos'
        source_file_name = f'{service_name}.json'
        target_file_name = f'{service_name}.proto'
        source_file_path = os.path.join(source_folder, source_file_name)
        target_file_path = os.path.join(target_folder, target_file_name)
        from_json_to_proto(source_file_path, target_file_path)
    print(">>>>[INFO] Step2: Generate proto file  From ../Json/{service_name}.json TO ../protos/{service_name}.proto")
    # Denpend on extracted_json file or code ---> class template file
    for service_name in services_name:
        source_folder = './Json'
        target_folder = './rpc_server_inc'
        source_file_name = f'{service_name}.json'
        target_file_name = f'{service_name}_impl.h'
        source_file_path = os.path.join(source_folder, source_file_name)
        target_file_path = os.path.join(target_folder, target_file_name)
        jinjaTemplate2IMPL_Class(source_file_path, target_file_path)
    print(">>>>[INFO] Step3: Generate impl class file From ../Json/{service_name}.json TO ../rpc_server_inc/{service_name}_impl_.h")
    # TODO: Generate ../rpc_client_inc/{service_name}_client_.h
    for service_name in services_name:
        source_folder = './Json'
        target_folder = './rpc_client_inc'
        source_file_name = f'{service_name}.json'
        target_file_name = f'{service_name}_client.h'
        source_file_path = os.path.join(source_folder, source_file_name)
        target_file_path = os.path.join(target_folder, target_file_name)
        jinjaTemplate2Client_Class(source_file_path, target_file_path)
    print(">>>>[INFO] Step3: Generate Client class file From ../Json/{service_name}.json TO ../rpc_client_inc/{service_name}_client_.h")

    # Generate ServerMain .cpp file
    # for service_name in services_name:
    # Eg: services_name = ['atomic_service_sfzt', 'atomic_service_skzt', 'atomic_service_mbsb']
    target_folderv = './src'
    target_file_namev = f'{server_name}.cpp' # get server name from ServerBaseInfo.json
    target_file_pathv = os.path.join(target_folderv, target_file_namev)
    genServerMainCpp(services_name, target_file_pathv)
    print(">>>>[INFO] Step4: Generate ServerMain.cpp file From ../Json/ *_impl_template.j2  TO  ../src/{}.cpp".format(server_name))

    # TODO: Generate ClientMain.cpp file
    target_folderp = './src'
    target_file_namep = 'ClientMain.cpp' # depende on personal setting
    target_file_pathp = os.path.join(target_folderp, target_file_namep)
    genClientMainCpp(services_name, target_file_pathp)
    print(">>>>[INFO] Step4: Generate ClientMain.cpp file From ../Json/ *_impl_template.j2  TO  ../src/{}".format(target_file_namep))

    # Generate atom .h file and .cpp file
    # for service_name in services_name:
    #     json_folder = './Json'
    #     atom_json_file_name = f'{service_name}.json'
    #     atom_json_file = os.path.join(json_folder, atom_json_file_name)
    #     # Generate atom .h file and .cpp file
    #     out_cpp_path = './atom_src'
    #     out_h_path = './atom_inc'
    #     Json2AtomInterface.generate_atom_files(atom_json_file, out_cpp_path, out_h_path)
    # print(">>>>")
    # print(">>>>[INFO] Step5: Generate atom .h file and .cpp file From ../Json/{service_name}.json TO ../atom_inc/{service_name}.h and ../atom_inc/{service_name}.cpp")

    # Generate AsyncServer AsyncServerMain.cpp
    async_main_name = "AsyncServerMain"
    target_folder = './src'
    output_file_name = f'{async_main_name}.cpp' # read AsyncServer Name from ServerBaseInfo.json  
    output_file_path = os.path.join(target_folder, output_file_name)
    AsyncServerTemplate2_AsyncServerMain(output_file_path)
    print(">>>>")
    print(f">>>>[INFO] Step6: Generate AsyncServerMain.cpp file From ../Jinja2/async_server_template.j2 TO {async_main_name}.cpp\n")

    print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Generate file and code Successful >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n")
    return server_name, services_name

if __name__ == "__main__":
    ServerBaseInfo_json_file = "ServerBaseInfo.json"
    # main(ServerBaseInfo_json_file)
    # Test Template
    server_name, services_name = parse_ServerBaseInfo_json(ServerBaseInfo_json_file)
    print("Step1: parse ServerBaseInfo.json")
    # print(services_name)
    # Generate proto file
    for service_name in services_name:
        source_folder = '../Json'
        target_folder = '../protos'
        source_file_name = f'{service_name}.json'
        target_file_name = f'{service_name}.proto'
        source_file_path = os.path.join(source_folder, source_file_name)
        target_file_path = os.path.join(target_folder, target_file_name)
        from_json_to_proto(source_file_path, target_file_path)
    print("Step2: Generate proto file  From ../Json/{service_name}.json TO ../protos/{service_name}.proto")
    # Generate extract json file or code ---> class template file
    for service_name in services_name:
        source_folder = '../Json'
        target_folder = '../rpc_inc'
        source_file_name = f'{service_name}.json'
        target_file_name = f'{service_name}_impl.h'
        source_file_path = os.path.join(source_folder, source_file_name)
        target_file_path = os.path.join(target_folder, target_file_name)
        jinjaTemplate2IMPL_Class(source_file_path, target_file_path)
    print("Step3: Generate impl class file From ../Json/{service_name}.json TO ../rpc_inc/{service_name}impl_.h")
    # Generate ServerMain .cpp file
    # for service_name in services_name:
    # Eg: services_name = ['atomic_service_sfzt', 'atomic_service_skzt', 'atomic_service_mbsb']
    target_folderv = '../src'
    target_file_namev = f'{server_name}.cpp'
    target_file_pathv = os.path.join(target_folderv, target_file_namev)
    genServerMainCpp(services_name, target_file_pathv)
    print("Step4: Generate server_main.cpp file From ../Json/ *_impl_template.j2  TO  ../src/serverMain.cpp")
    print("Generate file and code Successful")


    # Release Version
"""
    services_name = parse_ServerBaseInfo_json("./ServerBaseInfo.json")
    print("Step1: parse ServerBaseInfo.json")
    # print(services_name)
    # Generate proto file
    for service_name in services_name:
        source_folder = '../Json'
        target_folder = '../protos'
        source_file_name = f'{service_name}.json'
        target_file_name = f'{service_name}.proto'
        source_file_path = os.path.join(source_folder, source_file_name)
        target_file_path = os.path.join(target_folder, target_file_name)
        from_json_to_proto(source_file_path, target_file_path)
        # print("Step2: Generate proto file  From ../Json/{service_name}.json TO ../protos/{service_name}.proto")
        # Generate extract json file or code ---> class template file

        source_folder = '../Json'
        target_folder = '../rpc_inc'
        source_file_name = f'{service_name}.json'
        target_file_name = f'{service_name}_impl.h'
        source_file_path = os.path.join(source_folder, source_file_name)
        target_file_path = os.path.join(target_folder, target_file_name)
        jinjaTemplate2IMPL_Class(source_file_path, target_file_path)
        # print("Step3: Generate impl class file From ../Json/{service_name}.json TO ../rpc_inc/{service_name}impl_.h")
    # Generate serverMain .cpp file
    print("Generate file and code Successful")

"""