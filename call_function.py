from google.genai import types
from config import WORKING_DIR
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python import schema_run_python_file
from functions.write_file import schema_write_file

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)

def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    new_args = function_call_part.args
    new_args["working_directory"] = WORKING_DIR

    match function_name := function_call_part.name:
        case "get_files_info":
            from functions.get_files_info import get_files_info
            function_result = get_files_info(**new_args)
        case "get_file_content":
            from functions.get_file_content import get_file_content
            function_result = get_file_content(**new_args)
        case "run_python_file":
            from functions.run_python import run_python_file
            function_result = run_python_file(**new_args)
        case "write_file":
            from functions.write_file import write_file
            function_result = write_file(**new_args)
        case _:
            return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=function_name,
                        response={"error": f"Unknown function: {function_name}"},
                    )
                ],
            )
            
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )
