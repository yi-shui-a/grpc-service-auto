#!/root/venv/bin/python

import subprocess

# from jinja2.Services2Server import main

import sys
import os

# get the current directory
current_path = os.path.abspath(__file__)
print(current_path)
# get the parent directory
parent_dir = os.path.dirname(current_path)

# add subdirectory to sys.path
subdirectory_path = os.path.join(parent_dir, 'subdirectory')
sys.path.append("./Jinja2")

# import the module from the subdirectory
# import module
import Services2Server
import logo
# import [ main() ] function from Services2Server
# Services2Server.main()

def makeServerClient(array_values):
    # Define the make command and the variable you want to pass as an argument
    # make_command = "make"
    # variable_name = "VARIABLE_NAME"
    # variable_value = "value"
    array_str = ' '.join(array_values)
    make_command = ['make', f'MY_ARRAY={array_str}']
    # Construct the command with the argument
    # Here, we're assuming the Makefile is in the current directory
    # If the Makefile is in a different directory or has a different name, you need to specify it with the -f flag
    # command_with_args = [make_command, f"{variable_name}={variable_value}" , "-f", "Makefile"] # error !!!!!
    # command_with_args = subprocess.run(make_command, capture_output=True, text=True)

    # Execute the make command
    try:
        # subprocess.run() will execute the command and wait for it to complete
        # check=True means that if the command fails (returns a non-zero exit code), Python will raise an exception
        result = subprocess.run(make_command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Print the standard output
        print("Standard Output:\n", result.stdout)

    except subprocess.CalledProcessError as e:
        # Handle the case where the command execution fails
        print("Command execution failed:", e)
        print("Standard Output:\n", e.stdout)
        print("Standard Error:\n", e.stderr)

def run_make(array_values):
    # array values should be a list of strings
    array_str = ' '.join(array_values)
    # extract the first element
    first_element = array_values[0]
    second_element = array_values[1]
    # make cmd with variables
    make_command = [
        'make',
        f'MY_ARRAY={array_str}',
        f'FIRST_ELEMENT={first_element}', # ServerMain
        f'SECOND_ELEMENT={second_element}', # ClientMain
        f'REST_OF_ARRAY={" ".join(array_values[2:])}'
    ]
    # usee subprocess.run to execute the make command
    result = subprocess.run(make_command, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("Make command executed successfully.")
        print("Output:", result.stdout)
    else:
        print("Error occurred while executing make command.")
        print("Error output:", result.stderr)

def  run_make_all(server_dependencies, client_dependencies, async_server_dependencies):
    # array values should be a list of strings
    server_dependencies_str = ' '.join(server_dependencies)
    client_dependencies_str = ' '.join(client_dependencies)
    async_server_dependencies_str = ' '.join(async_server_dependencies)

    # print(server_dependencies_str,'\n')
    # print(client_dependencies_str,'\n')
    # print(async_server_dependencies_str,'\n')
    # exit()

    # make cmd with variables
    make_command = [
        'make',
        f'SERVER_DEPEND_ELEMENTS={server_dependencies_str}',
        f'CLIENT_DEPEND_ELEMENTS={client_dependencies_str}',
        f'ASYNC_SERVER_DEPEND_ELEMENTS={async_server_dependencies_str}',
    ]
    # usee subprocess.run to execute the make command
    result = subprocess.run(make_command, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("Make command executed successfully.")
        print("Output:", result.stdout)
    else:
        print("Error occurred while executing make command.")
        print("Error output:", result.stderr)


if __name__ == "__main__":
    # makeServerClient(['element1', 'element2', 'element3'])
    # $(OBJS_PATH)/my_service.pb.o $(OBJS_PATH)/my_service.grpc.pb.o $(OBJS_PATH)/Aserver.o
    # define an array of values
    ServerBaseInfo_json_file = "./Jinja2/ServerBaseInfo.json"
    # TODO: Step1 ServerBaseInfo.json config info to genCode
    server_name, services_name =  Services2Server.main(ServerBaseInfo_json_file)

    print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Compiling  Exectuable file ...... >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n")
    print("Running run_make.py ... \n")
    print("Server_name: ",server_name)
    print("Services_name: ",services_name)

    input_array_values = ['ServerMain', 'ClientMain']   
    for service_name in services_name:
        input_array_values.append(f"$(OBJS_PATH)/{service_name}.pb.o")
        input_array_values.append(f"$(OBJS_PATH)/{service_name}.grpc.pb.o")
        input_array_values.append(f"$(OBJS_PATH)/{service_name}.o") # *.atom_interface.o

    input_array_values.append(f"$(OBJS_PATH)/{server_name}.o")
    # input_parameter = [ f"{service_name}.pb.o" ,f"{service_name}.grpc.pb.o" ,  for service_name in services_name ]
    # print("input_array_values= {} \n".format(input_array_values))
    # array_values = ['ServerMain', 'ClientMain', '$(OBJS_PATH)/my_service.pb.o', '$(OBJS_PATH)/my_service.grpc.pb.o', '$(OBJS_PATH)/Aserver.o']
    # run_make(array_values)
    # TODO: Step2 running makefile
    # run_make(input_array_values)


    # TODO: Step3 running make generate [server and client] executable files
    server_dependencies = []
    client_dependencies = []
    async_server_dependencies = []

    for service_name in services_name:
        server_dependencies.append(f"$(OBJS_PATH)/{service_name}.pb.o")
        server_dependencies.append(f"$(OBJS_PATH)/{service_name}.grpc.pb.o")
        server_dependencies.append(f"$(OBJS_PATH)/{service_name}.o")

        client_dependencies.append(f"$(OBJS_PATH)/{service_name}.pb.o")
        client_dependencies.append(f"$(OBJS_PATH)/{service_name}.grpc.pb.o")
        client_dependencies.append(f"$(OBJS_PATH)/{service_name}.o")

        async_server_dependencies.append(f"$(OBJS_PATH)/{service_name}.pb.o")
        async_server_dependencies.append(f"$(OBJS_PATH)/{service_name}.grpc.pb.o")
        async_server_dependencies.append(f"$(OBJS_PATH)/{service_name}.o")

    server_dependencies.append(f"$(OBJS_PATH)/{server_name}.o")
    client_dependencies.append("$(OBJS_PATH)/ClientMain.o")
    async_server_dependencies.append("$(OBJS_PATH)/AsyncServerMain.o")
    
    run_make_all(server_dependencies, client_dependencies, async_server_dependencies)

    # logo.print_logo_two()
    print("Makefile run successfully")

