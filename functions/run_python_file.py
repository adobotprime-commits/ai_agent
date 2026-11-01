import os
import subprocess

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Runs a python script file path relative to the working directory, given a list of arguments to include in the run command",
        "parameters": {
            "required": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "File path for the python script to run, relative to the working directory",
                    },
                },
            },
            "optional": {
                "type": "object",
                "properties": {
                    "args":{
                        "type": "array[string]",
                        "description": "Array of string items to be used as arguments in the run command. Optional"
                    },
                },
            },
        },
    },
}

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
        if not os.path.isfile(target_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if os.path.commonpath([target_path, working_dir_abs]) != working_dir_abs:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not file_path.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_path]
        if args is not None:
            command.extend(args)

        completed_info = subprocess.run(command, capture_output=True, text=True, timeout=30, cwd=working_directory)
        output_str = ""
        if completed_info.returncode != 0:
            output_str += f"Process exited with code {completed_info.returncode}\n"
        if completed_info.stdout == None and completed_info.stderr == None:
            output_str += "No output produced\n"
        else:
            output_str += f'STDOUT:{completed_info.stdout}\nSTDERR:{completed_info.stderr}'
        return output_str

    except Exception as e:
        return f'Error: executing Python file: {e}'
