import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

def main():
    load_dotenv()

    api_key = os.environ.get("GEMINI_API_KEY")

    model = "gemini-2.0-flash-001"


    client = genai.Client(api_key=api_key)

    args = sys.argv
    if len(args) < 2:
        print("Usage: python main.py <prompt>")
        sys.exit(1)
    prompt = args[1]

    messages = [
        types.Content(role="user", parts=[types.Part(text=prompt)]),
    ]

    response = client.models.generate_content(model=model, contents=messages)

    print("Response:")
    print(response.text)


    if "--verbose" in args:
        print(f"User prompt: {prompt}")
        metadata = response.usage_metadata
        print(f"Prompt tokens: {metadata.prompt_token_count}")
        print(f"Response tokens: {metadata.candidates_token_count}")

if __name__ == "__main__":
    main()