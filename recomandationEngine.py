import json
from openai import OpenAI

# Initialize DeepSeek client
client = OpenAI(
    api_key="API_KEY",
    base_url="https://api.deepseek.com"  # Required for DeepSeek
)

# Prompt template with escaped braces
DEEPSEEK_PROMPT = """
You are a fashion assistant. A user is giving you their age, weight, height, skin color, and a list of clothing items they have.

You must recommend 3 OUTFITS OF THE DAY based on their attributes and the event they are attending.

Always include:
- 1 shirt
- 1 pant
- 1 pair of shoes
- 1 accessory (like shades, belt, or watch)

Match clothing to skin color, age group, and occasion.

Return ONLY the output in this JSON format:
[
  {{
    "shirt": "...",
    "pant": "...",
    "shoes": "...",
    "shades": "..."
  }},
  ...
]

Here is the input JSON:
{input_json}
"""

def load_user_json(path):
    with open(path, "r") as f:
        return json.load(f)

def generate_recommendations(user_data):
    prompt = DEEPSEEK_PROMPT.format(input_json=json.dumps(user_data, indent=2))

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "You are a fashion recommendation engine."},
            {"role": "user", "content": prompt}
        ],
        stream=False
    )

    content = response.choices[0].message.content
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        print("⚠️ Could not parse JSON. Raw content returned:\n", content)
        return []

if __name__ == "__main__":
    file_path = r"C:\Users\rohan\Desktop\ootd\OOTD\sampleInput.json"
    user_json = load_user_json(file_path)
    outfits = generate_recommendations(user_json)

    print("👕 Recommended Outfits:")
    print(json.dumps(outfits, indent=2))
