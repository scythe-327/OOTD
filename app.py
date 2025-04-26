import json
from flask import Flask, request, jsonify
from groq import Groq

# Set up your Groq client
client = Groq(api_key=os.getenv("API_KEY"))

# Define the Flask app
app = Flask(__name__)

# Define the prompt template
PROMPT_TEMPLATE = """
You are an experienced fashion assistant. A user is giving you their age, weight, height, skin color, and a list of clothing items they own.

They are also telling you the event they are attending. Based on that, recommend **3 stylish outfits**.

Each outfit must include:
- 1 shirt
- 1 pant
- 1 pair of shoes
- 1 accessory (like shades, belt, or watch)

<Reasoning>
Apply Theory of Mind and Color Theory to understand the user’s fashion preferences, which is given in the prompt, and the context of the event. Use strategic reasoning to ensure outfits are both aesthetically pleasing and practical, balancing the user’s emotional tone and logical needs, which is provided in the prompt.
</Reasoning>

Please provide **exactly 3 outfits** in proper JSON format, each containing only one shirt, one pant, one pair of shoes, and one accessory. Do not repeat any key or list multiple items for a single category.

Here is the input:
{user_input}
NOTE THAT YOU DIRECTLY START WITH THE RECOMENDATION JSON, DO NOT GIVE ANY TEXTS IN THE BEGINING , START DIRECTLY WITH JSON,DO NOT EVEN USE THE WORD JSON
"""
import json
import re

def clean_response(response_text):
    try:
        # First, try to extract JSON inside a ```json ... ``` code block
        json_match = re.search(r"```\s*```", response_text, re.DOTALL)
        if json_match:
            response_text = json_match.group(1).strip()         
        else:
            print("⚠️ No JSON code block found, trying to parse entire response.")

        # Now try to load the cleaned JSON
        outfits = json.loads(response_text)
        return outfits

    except Exception as e:
        print(f"⚠️ Failed to parse JSON: {e}")
        return [{"error": "Failed to generate recommendations due to malformed response."}]

# Generate outfit recommendations
def generate_outfit_recommendations(user_data):
    prompt = PROMPT_TEMPLATE.format(user_input=json.dumps(user_data, indent=2))

    # Send the request to the API
    try:
        chat_completion = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=[{"role": "user", "content": prompt}]
        )

        # Get the API response
        response = chat_completion.choices[0].message.content
        print("API Response:", response)  # Log the raw response
        
        # Clean and parse the response into outfits
        outfits = clean_response(response)
        return outfits
    
    except Exception as e:
        print(f"⚠️ Error during API call: {e}")
        return [{"error": "Failed to generate recommendations due to an API issue."}]

# Define the endpoint to receive POST requests
@app.route('/generate-outfit', methods=['POST'])
def get_outfit():
    try:
        # Log the received input for debugging
        user_data = request.get_json()
        print("Received user data:", user_data)

        # Get outfit recommendations
        outfits = generate_outfit_recommendations(user_data)
        print("Generated outfits:", outfits)

        # Return the recommendations as JSON
        return jsonify(outfits)

    except Exception as e:
        # Catch any exception and print the full error
        print(f"⚠️ Error processing the request: {e}")
        # Optionally print the traceback for deeper insight
        import traceback
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 400

# Run the app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
