import os
import argparse
from dotenv import load_dotenv
from openai import OpenAI

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
        {"role": "user", "content": args.user_prompt},
    ]

    # Get response from AI client
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
    )

    # Print output to console
    if response.usage is None:
        raise RuntimeError("API request failed")

    if args.verbose is True:
        print(f'User prompt: {args.user_prompt}')
        print(f'Prompt tokens: {response.usage.prompt_tokens}')
        print(f'Response tokens: {response.usage.completion_tokens}')

    print(f'Response: \n{response.choices[0].message.content}')


if __name__ == "__main__":
    main()
