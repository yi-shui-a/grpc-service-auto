import subprocess

def make_server_client():
    # Define the make command and the variable you want to pass as an argument
    make_command = "make"
    variable_name = "VARIABLE_NAME"
    variable_value = "value"

    # Construct the command with the argument
    # Here, we're assuming the Makefile is in the current directory
    # If the Makefile is in a different directory or has a different name, you need to specify it with the -f flag
    command_with_args = [make_command, f"{variable_name}={variable_value}"]

    # Execute the make command
    try:
        # subprocess.run() will execute the command and wait for it to complete
        # check=True means that if the command fails (returns a non-zero exit code), Python will raise an exception
        result = subprocess.run(command_with_args, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Print the standard output
        print("Standard Output:\n", result.stdout)

    except subprocess.CalledProcessError as e:
        # Handle the case where the command execution fails
        print("Command execution failed:", e)
        print("Standard Output:\n", e.stdout)
        print("Standard Error:\n", e.stderr)