import os
import argparse
import json
from dotenv import load_dotenv
from openai import OpenAI
from call_function import available_functions, call_function
from prompts import system_prompt

def main():

    # Load API key from .env file
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")

    # Check if API key was retrieved
    if api_key is None:
        raise RuntimeError("invalid API key")
    print("API key loaded")

    # Get message from user via argparse
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    # Connect to AI client
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]

    # Loop AI Agent

    for _ in range(20):
        # Get response from AI client
        response = client.chat.completions.create(
            model="openrouter/free",
            messages=messages,
            tools=available_functions,
            temperature=0,
        )

        if response.usage is None:
            raise RuntimeError("API request failed")

        if args.verbose is True:
            print(f'User prompt: {args.user_prompt}')
            print(f'Prompt tokens: {response.usage.prompt_tokens}')
            print(f'Response tokens: {response.usage.completion_tokens}')

        # Handle function calls
        message = response.choices[0].message
        messages.append(message)
        if message.tool_calls:
            for tool_call in message.tool_calls:
                result_message = call_function(tool_call)
                if result_message["content"] is None:
                    raise Exception(f"No content returned by function call to {tool_call.function.name}")
                if args.verbose is True:
                    print(f"-> {result_message['content']}")
                messages.append(result_message)
        # Print output to console
        else:
            print(f'Response: \n{message.content}')
            return

    print("-- Program ended, Agent could not complete request within 20 responses --")
    exit(1)


if __name__ == "__main__":
    main()
