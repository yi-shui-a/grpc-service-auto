#!/root/venv/bin/python

import json
import os

import jinja2
# import template
from jinja2 import Template, FileSystemLoader, Environment

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
    # print("server_name:",server_name)
    for service in data.get('service', []):  # use .get() avoid KeyError
        service_names.append(service['name'])
    # print("service_names:",service_names)
    return server_name, service_names


def extract_service_json_info(source_file_name):
    # json_file_path = 'sj_service.json'
    # read JSON and convert into a Python dictionary
    # with open(source_file_name, 'r') as file:
    #     json_data = json.load(file)
    try:
        with open(source_file_name, 'r') as json_file:
            json_data = json.load(json_file)
    except json.JSONDecodeError as err:
        print(f"JSONDecodeError: {err}")
        return []

    # extract package info
    package_info = {
        "syntax": json_data.get("syntax"),
        "package_name": json_data.get("package"),
        "service_name": json_data.get("service_name"),
        "request_name": json_data.get("request"),
        "reply_name": json_data.get("reply"),
        "atom_interface": json_data.get("atom_interface"),
        "atom_name": json_data.get("atom_name")
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
        "package": package_info,
        "messages": messages_dict,
        "services": services_info
    }
    # print extracted_info (used debug)
    # print(json.dumps(extracted_info, indent=2))

    # with open("async_server_template.json", 'w') as outfile:
    #     json.dump(extracted_info, outfile, indent=2)
    # print(f'Extracted data has been written to {target_file_path}')
    return extracted_info

def extractServerBase2AsyncTemplate():
    serverBaseJson = "./ServerBaseInfo.json"
    server_name, services_name = parse_ServerBaseInfo_json(serverBaseJson)
    source_folder = '../Json'
    all_services_info = []
    for service in services_name:
        source_file_name = f'{service}.json'    
        source_file_path = os.path.join(source_folder, source_file_name)
        all_services_info.append(extract_service_json_info(source_file_path))

    with open("async_server_template.json", 'w') as outfile:
        json.dump(all_services_info, outfile, indent=2)
    return all_services_info

def AsyncServerTemplate2_AsyncServerMain(async_main_template_output_name):
    # jinja2 template loader path
    j2_loader = FileSystemLoader('./')
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

def AsyncServerTemplate2_AsyncServerMain_v(async_main_template_output_name):
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

if __name__ == "__main__":
    # file_path_name = "ServerBaseInfo.json"
    # server_name, services_name = parse_ServerBaseInfo_json(file_path_name)
    # # print(extract_data_from_json(json_file))

    extractServerBase2AsyncTemplate()

    async_main_name = "AsyncServerMain"
    target_folder = './'
    output_file_name = f'{async_main_name}.cpp'    
    output_file_path = os.path.join(target_folder, output_file_name)

    AsyncServerTemplate2_AsyncServerMain(output_file_path)