import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load environment variables
load_dotenv()

# Get Gemini API key
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env")

# Create Gemini client
client = genai.Client(api_key=api_key)

MODEL = "gemini-2.5-flash"


def call(prompt, temperature):
    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=temperature
        ),
    )

    print("=" * 70)
    print(f"Temperature: {temperature}")
    print("=" * 70)

    print("\nPrompt:")
    print(prompt)

    print("\nResponse:")
    print(response.text)

    # Token usage details
    usage = response.usage_metadata

    print("\nToken Usage:")
    print("-" * 70)
    print(f"Prompt Tokens     : {usage.prompt_token_count}")
    print(f"Thought Tokens    : {getattr(usage, 'thoughts_token_count', 0)}")
    print(f"Completion Tokens : {usage.candidates_token_count}")
    print(f"Total Tokens      : {usage.total_token_count}")

    print()

    return response


# Strong constraint-based prompt
prompt = """
Write exactly one tagline for a coffee shop.
Output only the tagline.
Do not provide options.
Do not include explanations.
Do not add labels or extra text.
"""


# Run with low randomness
call(prompt, temperature=0.0)

# Run with higher randomness
call(prompt, temperature=1.0)


#OUTPUT
'''
======================================================================
Temperature: 0.0
======================================================================

Prompt:

Write exactly one tagline for a coffee shop.
Output only the tagline.
Do not provide options.
Do not include explanations.
Do not add labels or extra text.


Response:
Your Daily Brew, Your Perfect Moment.

Token Usage:
----------------------------------------------------------------------
Prompt Tokens     : 39
Thought Tokens    : 30
Completion Tokens : 8
Total Tokens      : 77

======================================================================
Temperature: 1.0
======================================================================

Prompt:

Write exactly one tagline for a coffee shop.
Output only the tagline.
Do not provide options.
Do not include explanations.
Do not add labels or extra text.


Response:
Your Daily Ritual.

Token Usage:
----------------------------------------------------------------------
Prompt Tokens     : 39
Thought Tokens    : 662
Completion Tokens : 4
Total Tokens      : 705

'''
