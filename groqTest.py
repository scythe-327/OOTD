import json
from groq import Groq

# ✅ Your Groq API key
client = Groq(
    api_key="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"
)

# 🔁 Prompt Template with Escaped Braces
PROMPT_TEMPLATE = """
You are a experienced fashion assistant. A user is giving you their age, weight, height, skin color, and a list of clothing items they own.

They are also telling you the event they are attending. Based on that, recommend **3 stylish outfits**.

Each outfit must include:
- 1 shirt
- 1 pant
- 1 pair of shoes
- 1 accessory (like shades, belt, or watch)
<Reasoning>
Apply Theory of Mind and Color Theory to understand the user’s fashion preferences which is given in the prompt and the context of the event. Use strategic reasoning to ensure outfits are both aesthetically pleasing and practical, balancing the user’s emotional tone and logical needs which is provided in the prompt.
</Reasoning>
"Please provide **exactly 3 outfits** in proper JSON format, each containing only one shirt, one pant, one pair of shoes, and one accessory. Do not repeat any key or list multiple items for a single category."
Your response must be in **pure JSON** like this and should only have 3 top recomandation:
[
  {{
    "shirt": "...",
    "pant": "...",
    "shoes": "...",
    "shades": "...",
    "accessories":"..."
  }},
  ...
]

Here is the input:
{user_input}
"""

# 📂 Load the user input JSON from file
def load_user_json(path):
    with open(path, "r") as file:
        return json.load(file)

# 🧠 Generate outfit recommendations using Groq
def generate_outfit_recommendations(user_data):
    prompt = PROMPT_TEMPLATE.format(user_input=json.dumps(user_data, indent=2))

    chat_completion = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    response = chat_completion.choices[0].message.content

    try:
        outfits = json.loads(response)
    except json.JSONDecodeError:
        print("⚠️ Failed to parse JSON. Here's the raw response:\n", response)
        outfits = []

    return outfits

# 🚀 Run the engine
if __name__ == "__main__":
    file_path = r"C:\Users\rohan\Desktop\ootd\OOTD\sampleInput.json"
    user_json = load_user_json(file_path)
    outfits = generate_outfit_recommendations(user_json)

    print("👗 Outfit Recommendations:")
    print(json.dumps(outfits, indent=2))
