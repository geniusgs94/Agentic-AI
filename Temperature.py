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
============================================================
Temperature: 0.0
------------------------------------------------------------
Response:
Here are a few options, playing on different angles:

**Focus on Quality/Taste:**
*   Crafting the perfect cup, just for you.
*   Exceptional coffee, every single time.
*   Where passion meets the perfect pour.

**Focus on Experience/Atmosphere:**
*   Your cozy corner for exceptional coffee and connection.
*   Unwind, connect, and savor your perfect moment.
*   More than just coffee, it's your daily escape.

**Focus on Benefit/Energy:**
*   Start your day brighter, one delicious sip at a time.
*   Fueling your day, one perfect cup at a time.
*   Where every sip sparks your day.

**Simple & Direct:**
*   Your daily ritual, perfected.
*   Your daily dose of delicious.

Choose the one that best fits the specific vibe and mission of the coffee shop!

Token Usage:
Prompt Tokens    : 12
Completion Tokens: 192
Total Tokens     : 1408

============================================================
Temperature: 1.0
------------------------------------------------------------
Response:
Here are a few options, playing on different angles:

**Focus on Quality/Product:**
*   Crafting your perfect cup, every single time.

**Focus on Experience/Comfort:**
*   Your daily escape, steeped in comfort and community.

**Focus on Energy/Start:**
*   Ignite your day with the perfect cup.

**Focus on Simplicity/Daily Ritual:**
*   Your daily ritual, perfected.

**Focus on Community/Connection:**
*   Connecting people, one cup at a time.

**Short & Sweet:**
*   Where every sip feels like home.

Choose the one that best fits your shop's unique vibe!

Token Usage:
Prompt Tokens    : 12
Completion Tokens: 142
Total Tokens     : 1273

'''
