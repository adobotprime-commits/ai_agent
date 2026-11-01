import os

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Writes a content string to a given file path relative to the working directory, overwriting previous content and creating any missing directories",
        "parameters": {
            "required": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "File path to write the content string to, relative to the working directory. Any missing directories in the file path will be created",
                    },
                    "content": {
                        "type": "string",
                        "description": "Content to write to the file, in string format"
                    }
                },
            },
        },
    },
}

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
        if os.path.isdir(target_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        if os.path.commonpath([target_path, working_dir_abs]) != working_dir_abs:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        os.makedirs(os.path.dirname(target_path),exist_ok=True)

        with open(target_path, "w") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f'Error: {e}'
