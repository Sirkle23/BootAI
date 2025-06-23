import os.path
from google.genai import types
from config import MAX_CHARS

def get_file_content(working_directory, file_path):

    abs_working_dir = os.path.abspath(working_directory)
    target_file = os.path.abspath(os.path.join(abs_working_dir, file_path))

    if not target_file.startswith(abs_working_dir):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(target_file):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    print(os.path.getsize(target_file))
    try:
        with open(target_file, "r") as f:
            file_content_string = f.read(MAX_CHARS)

        if os.path.getsize(target_file) > MAX_CHARS:
            file_content_string += f'\n[...File "{file_path}" truncated at {MAX_CHARS} characters]'

    except Exception as e:
        return f"Error showing file content: {e}"

    return file_content_string

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Shows the contents of a certain file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path specifying the file of which the contents should be displayed, relative to the working directory.",
            ),
        },
    ),
)