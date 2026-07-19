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
