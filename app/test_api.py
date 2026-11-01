
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

model = os.getenv("OPENAI_MODEL", "openai/gpt-4o-mini")

response = client.chat.completions.create(
    model=model,
    messages=[
        {
            "role": "user",
            "content": "Explain what a multilingual AI agent does in two sentences."
        }
    ]
)

print("\nModel:", model)
print("\nResponse:")
print(response.choices[0].message.content)
