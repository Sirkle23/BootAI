import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path):

    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(abs_file_path):
        return f'Error: File "{file_path}" not found.'

    if not abs_file_path.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        output = subprocess.run(['python3', abs_file_path], timeout=30, capture_output=True, cwd=abs_working_dir, text=True)

        if output.stdout == b'' and output.stderr == b'':
            return f'No output produced.'

        str_out = ""
        #str_out += f'STDOUT: {output.stdout.decode('utf-8')}\n'
        #str_out += f'STDERR: {output.stderr.decode('utf-8')}\n'
        str_out += f'STDOUT: {output.stdout}\n'
        str_out += f'STDERR: {output.stderr}\n'
        if output.returncode != 0:
            str_out += f'Process exited with code {output.returncode}.'
        return str_out

    except Exception as e:
        return f"Error: Executing Python file: {e}"

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a certain python file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path specifying the file that should be run, relative to the working directory.",
            ),
        },
    ),
)