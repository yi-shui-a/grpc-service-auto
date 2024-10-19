#!/root/venv/bin/python

import json
import sys
import os
def generate_proto_file(input_filename, output_filename):
    # Load the JSON data from the input file
    with open(input_filename, 'r') as json_file:
        data = json.load(json_file)
    
    # Start building the proto file content
    # proto_content = 'syntax = "{}";\n\n'.format(data['syntax'])
    # proto_content += 'package {};\n\n'.format(data['package'])
    proto_content = 'syntax = "{}";\n\n'.format(data['implement_rpc']['syntax'])
    proto_content += 'package {};\n\n'.format(data['implement_rpc']['package'])
    
    # Generate messages
    for msg in data['messages']:
        proto_content += 'message {} {{\n'.format(msg['name'])
        for field in msg['fields']:
            field_type = field['type']
            if 'repeated' in field and field['repeated']:
                field_type = 'repeated {}'.format(field_type)
            elif 'map' in field_type:
                # key_type, value_type = field_type[4:-1].split(',')
                # field_type = 'map<{}, {}>'.format(key_type.strip(), value_type.strip())
                field_type = 'map<{}, {}>'.format(field['key'], field['value'])
                # strip() methods are used to remove leading and trailing whitespaces
            proto_content += '  {} {} = {};\n'.format(field_type, field['name'], field['id'])
        proto_content += '}\n\n'
    
    # Generate services
    for srv in data['services']:
        proto_content += 'service {} {{\n'.format(srv['name'])
        for method in srv['methods']:
            method_type = 'rpc {} ({}) returns ({}) {{}}'.format(method['name'], method['requestType'], method['responseType'])
            # if method.get('serverStreaming', False):
            #     method_type = method_type.replace(')', 'stream )')
            # elif method.get('clientStreaming', False):
            #     method_type = method_type.replace('(', 'stream ')
            # elif method.get('bidirectionalStreaming', False):
            #     method_type = method_type.replace('(', 'stream ').replace(')', 'stream )')
            proto_content += '  {}\n'.format(method_type)
        proto_content += '}\n\n'
    
    # Write the generated proto content to the output file
    with open(output_filename, 'w') as output_file:
        output_file.write(proto_content)


def generate_proto_file_modified(input_filename, output_filename):
    # Load the JSON data from the input file
    with open(input_filename, 'r') as json_file:
        data = json.load(json_file)
    # Start building the proto file content
    proto_content = 'syntax = "{}";\n\n'.format(data['implement_rpc']['syntax'])
    proto_content += 'package {};\n\n'.format(data['implement_rpc']['package'])
    # Generate messages
    for msg in data['messages']:
        proto_content += 'message {} {{\n'.format(msg['name'])
        for field in msg['fields']:
            field_type = field['type']
            if 'repeated' in field and field['repeated']:
                field_type = 'repeated {}'.format(field_type)
            elif 'map' in field_type:
                field_type = 'map<{}, {}>'.format(field['key'], field['value'])
            proto_content += '  {} {} = {};\n'.format(field_type, field['name'], field['id'])
        proto_content += '}\n\n'
    # Generate services
    for srv in data['services']:
        proto_content += 'service {} {{\n'.format(srv['name'])
        for method in srv['methods']:
            method_type = 'rpc {} ({}) returns ({}) {{}}'.format(method['name'], method['requestType'], method['responseType'])
            proto_content += '  {}\n'.format(method_type)
        proto_content += '}\n\n'
    # Write the generated proto content to the output file
    with open(output_filename, 'w') as output_file:
        output_file.write(proto_content)

# generate_proto_file(json_filename, output_filename)
if __name__ == "__main__":
   
    source_folder = '../Json'
    target_folder = '../protos'
    source_file_name = 'atomic_service_dds.json'
    target_file_name = 'my_service_modified.proto'

    source_file_path = os.path.join(source_folder, source_file_name)
    target_file_path = os.path.join(target_folder, target_file_name)
    # generate_proto_file(source_file_path, target_file_path)
    generate_proto_file_modified(source_file_path, target_file_path)