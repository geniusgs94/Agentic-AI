import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load environment variables
load_dotenv()

# Create Gemini client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

MODEL = "gemini-2.5-flash"


def call(prompt, temperature):
    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=temperature
        ),
    )

    print("=" * 60)
    print(f"Temperature: {temperature}")
    print("-" * 60)
    print("Response:")
    print(response.text)

    print("\nToken Usage:")
    print(f"Prompt Tokens    : {response.usage_metadata.prompt_token_count}")
    print(f"Completion Tokens: {response.usage_metadata.candidates_token_count}")
    print(f"Total Tokens     : {response.usage_metadata.total_token_count}")
    print()

    return response


prompt = "Write a one-sentence tagline for a coffee shop."

# Deterministic
call(prompt, temperature=0.0)

# More creative
call(prompt, temperature=1.0)
