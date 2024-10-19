#!/root/venv/bin/python

import json
import os

def extract_json2template(source_file_name):
    
    # json_file_path = 'sj_service.json'
    # read JSON and convert into a Python dictionary
    with open(source_file_name, 'r') as file:
        json_data = json.load(file)

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
    # print extracted_info (used debug)
    # print(json.dumps(extracted_info, indent=2))

    # with open(target_file_name, 'w') as outfile:
    #     json.dump(extracted_info, outfile, indent=2)
    # print(f'Extracted data has been written to {target_file_path}')

    return extracted_info

def extract_json_info(source_file_name, target_file_name):
    
    # json_file_path = 'sj_service.json'
    # read JSON and convert into a Python dictionary
    with open(source_file_name, 'r') as file:
        json_data = json.load(file)
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
    with open(target_file_name, 'w') as outfile:
        json.dump(extracted_info, outfile, indent=2)
    print(f'Extracted data has been written to {target_file_path}')

    return extracted_info

if __name__ == "__main__":
    
    source_folder = '../Json'
    target_folder =  '../Json'

    name = "atomic_service_dds"

    source_file_name = f'{name}.json'
    target_file_name = f'extracted_{name}.json'

    source_file_path = os.path.join(source_folder, source_file_name)
    target_file_path = os.path.join(target_folder, target_file_name)
    extract_json_info(source_file_path, target_file_path)
   
