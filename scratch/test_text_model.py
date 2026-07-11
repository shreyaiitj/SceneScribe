import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(override=True)
api_key = os.environ.get("FIREWORKS_API_KEY")

client = OpenAI(
    base_url="https://api.fireworks.ai/inference/v1",
    api_key=api_key
)

scene_description = """The video captures a dynamic scene with natural lighting. 
Multiple characters or objects are visible in motion across the frame. 
The setting appears to be outdoors or in a well-lit environment."""

system_prompt = """You are a precise video captioning AI.
Your task: Generate captions in 4 distinct styles: "formal", "sarcastic", "humorous_tech", "humorous_non_tech".
For every caption, you must provide a confidence score between 0 and 100.

Your output MUST be a single valid JSON object. Do NOT wrap in markdown.
The JSON must have exactly these 4 keys: "formal", "sarcastic", "humorous_tech", "humorous_non_tech".
Each value must be an object with "caption" (string) and "confidence" (integer).
"""

user_content = f"Visual Scene Description:\n{scene_description}\n\nGenerate the 4 confidence-aware captions in JSON format."

try:
    response = client.chat.completions.create(
        model="accounts/fireworks/models/kimi-k2p6",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content}
        ],
        max_tokens=300,
        temperature=0.7
    )
    print("RAW RESPONSE:")
    print(response.choices[0].message.content)
except Exception as e:
    print("Error:", e)
