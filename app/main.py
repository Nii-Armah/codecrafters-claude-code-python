from .utils import get_tools, read_file

import argparse
import os
import sys

import json

from openai import OpenAI

API_KEY = os.getenv("OPENROUTER_API_KEY")
BASE_URL = os.getenv("OPENROUTER_BASE_URL", default="https://openrouter.ai/api/v1")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("-p", required=True)
    args = p.parse_args()

    if not API_KEY:
        raise RuntimeError("OPENROUTER_API_KEY is not set")

    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

    tools = get_tools()
    messages = {'role': 'user', 'content': args.p}

    while True:
        chat = client.chat.completions.create(
            model="anthropic/claude-haiku-4.5",
            messages=messages,
            tools=tools
        )

        if not chat.choices or len(chat.choices) == 0:
            raise RuntimeError("no choices in response")

        if not chat.choices[0].message.tool_calls:
            print(chat.choices[0].message.content)
            break

        else:
            for tool_call in chat.choices[0].message.tool_calls:
                tool_args = chat.choices[0].message.tool_calls[0].function.arguments
                args = json.loads(tool_args)
                file_content = read_file(args.get('file_path'))
                messages.append({'role': 'tool', 'tool_call_id': tool_call.id, 'content': file_content})



        # You can use print statements as follows for debugging, they'll be visible when running tests.
        print("Logs from your program will appear here!", file=sys.stderr)




if __name__ == "__main__":
    main()
