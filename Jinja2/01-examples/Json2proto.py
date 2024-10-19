import sys
import argparse
import json

def generate_proto_file(input_filename, output_filename):
    # Load the JSON data from the input file
    with open(input_filename, 'r') as json_file:
        data = json.load(json_file)
    
    # Start building the proto file content
    proto_content = 'syntax = "{}";\n\n'.format(data['syntax'])
    proto_content += 'package {};\n\n'.format(data['package'])
    
    # Generate messages
    for msg in data['messages']:
        proto_content += 'message {} {{\n'.format(msg['name'])
        for field in msg['fields']:
            field_type = field['type']
            if 'repeated' in field and field['repeated']:
                field_type = 'repeated {}'.format(field_type)
            elif 'map' in field_type:
                key_type, value_type = field_type[4:-1].split(',')
                field_type = 'map<{}, {}>'.format(key_type.strip(), value_type.strip())
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

def main():
    parser = argparse.ArgumentParser(description='Generate a .proto file from a JSON description.')
    parser.add_argument('input', type=str, help='Input JSON file')
    parser.add_argument('output', type=str, help='Output .proto file')
    args = parser.parse_args()
    
    generate_proto_file(args.input, args.output)
    print('Generated .proto file: {}'.format(args.output))

if __name__ == '__main__':
    main()

# python Json2protoV1.py hk_service.json hk_service.proto