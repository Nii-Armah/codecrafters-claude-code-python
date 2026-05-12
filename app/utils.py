import json
import os

def get_tools() -> list:
    script_path = os.path.dirname(os.path.abspath(__file__))
    tools_path = os.path.join(script_path, 'tools.json')
    with open(tools_path) as tools_file:
        return json.load(tools_file)