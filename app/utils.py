import json


def get_tools() -> list:
    with open('/app/tools.json') as tools_file:
        return json.load(tools_file)