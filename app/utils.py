import json
import os
import subprocess

def get_tools_specs() -> list:
    script_path = os.path.dirname(os.path.abspath(__file__))
    tools_path = os.path.join(script_path, 'tools.json')

    with open(tools_path) as tools_file:
        return json.load(tools_file)

def run_bash(command: str) -> bytes:
    result = subprocess.run([command], shell=True,  capture_output=True)
    return result.stdout or result.stderr


def read_file(file_path: str) -> str:
    with open(file_path) as file:
        return file.read()

def write_file(file_path: str, content: str) -> str:
    with open(file_path, 'w') as file:
        file.write(content)

    return f'Successfully wrote to {file_path}'