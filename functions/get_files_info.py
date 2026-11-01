import os

schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "required": {
                "type": "object",
                "properties": {
                    "directory": {
                        "type": "string",
                        "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                    },
                },
            },
        },
    },
}

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        if os.path.commonpath([target_dir, working_dir_abs]) != working_dir_abs:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        info_strings = []

        file_paths = os.listdir(target_dir)
        for path in file_paths:
            info_strings.append(f'- {path}: file_size={os.path.getsize(target_dir + "/" + path)} bytes, is_dir={os.path.isdir(target_dir + "/" + path)}')

        return "\n".join(info_strings)

    except Exception as e:
        return f'Error: {e}'
