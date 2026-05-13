from .utils import get_tools_specs, read_file, run_bash, write_file

import argparse
import json
import os

from openai import OpenAI


API_KEY = os.getenv('OPENROUTER_API_KEY')
BASE_URL = os.getenv('OPENROUTER_BASE_URL', default='https://openrouter.ai/api/v1')


tools_repo = {
    'ReadFile': read_file,
    'WriteFile': write_file,
    'RunBash': run_bash,
}


def main():
    p = argparse.ArgumentParser()
    p.add_argument('-p', required=True)
    args = p.parse_args()

    if not API_KEY:
        raise RuntimeError('OPENROUTER_API_KEY is not set')

    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)
    messages = [{'role': 'user', 'content': args.p}]

    while True:
        chat = client.chat.completions.create(
            model='anthropic/claude-haiku-4.5',
            messages=messages,
            tools=get_tools_specs()
        )

        if not chat.choices or len(chat.choices) == 0:
            raise RuntimeError('no choices in response')

        message = chat.choices[0].message
        messages.append({
            'role': 'assistant',
            'content': None,
            'tool_calls': message.tool_calls
        })

        if not message.tool_calls:
            print(message.content)
            break

        for tool_call in message.tool_calls:
            tool = tools_repo.get(tool_call.function.name)
            tool_args = json.loads(tool_call.function.arguments)
            result = tool(**tool_args)
            messages.append({'role': 'tool', 'tool_call_id': tool_call.id, 'content': result})


if __name__ == "__main__":
    main()
