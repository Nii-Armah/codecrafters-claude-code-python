import json
import os


def get_tools() -> list:
    print(os.listdir('..'))
    return []
    # with open('.tools.json') as tools_file:
        # return json.load(tools_file)