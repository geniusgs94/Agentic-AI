import time
from google import genai
from google.genai.errors import ServerError

client = genai.Client(api_key=api_key)

for attempt in range(5):
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents="What is an API?"
        )
        print(response.text)
        break

    except ServerError as e:
        print(f"Attempt {attempt + 1} failed: {e}")
        if attempt == 4:
            raise
        time.sleep(2 ** attempt)  # Exponential backoff