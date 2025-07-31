import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

OPEN_ROUTER_API_KEY = os.getenv('OPEN_ROUTER_API_KEY')
BASE_URL = "https://openrouter.ai/api/v1"
MODEL = 'google/gemini-flash-1.5'

response = requests.post(
    url=f"{BASE_URL}/chat/completions",
    headers={
        "Authorization": f"Bearer {OPEN_ROUTER_API_KEY}",
    },
    data = json.dumps({
        "model" : MODEL,
        "messages" : [
            {
                "role" : "user",
                "content" : "who is the founder of openai"
            }
        ]
    })
)

# print(response)
data = response.json()
print(data['choices'][0]['message']['content'])