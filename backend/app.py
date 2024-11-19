import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

API_URL = "https://api-inference.huggingface.co/models/openai-community/gpt2"
HF_API_KEY = "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"

headers = {"Authorization": f"Bearer {HF_API_KEY}"}

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return jsonify({
        "message": "Welcome to the Bio Generator API!",
        "instructions": "Use the /generate_bio/ui/hugging_face_API endpoint to generate a bio.",
        "method": "POST",
        "example_payload": {
            "preferences": {
                "career": "Software Developer",
                "personality": "Outgoing",
                "interests": "AI, gaming",
                "goals": "Find meaningful connections"
            }
        }
    })

@app.route('/generate_bio/ui/hugging_face_API', methods=['POST'])
def generate_bio():
    try:
        data = request.get_json(force=True)
        preferences = data.get("preferences", {})
        if not all(key in preferences for key in ['career', 'personality', 'interests', 'goals']):
            return jsonify({"error": "Missing required preferences"}), 400

        prompt = (
            f"Generate a short, engaging bio based on these preferences:\n"
            f"Career: {preferences.get('career', 'Not provided')}\n"
            f"Personality: {preferences.get('personality', 'Not provided')}\n"
            f"Interests: {preferences.get('interests', 'Not provided')}\n"
            f"Relationship Goals: {preferences.get('goals', 'Not provided')}."
        )

        response = requests.post(API_URL, headers=headers, json={"inputs": prompt})

        if response.status_code != 200:
            return jsonify({
                "error": f"Failed to generate bio. Status code: {response.status_code}",
                "details": response.json()
            }), 500

        result = response.json()
        if isinstance(result, list) and len(result) > 0:
            bio = result[0].get("generated_text", "Error: No generated text found")
        else:
            bio = "Error: Unexpected response format"

        return jsonify({"bio": bio})

    except requests.exceptions.RequestException as e:
        return jsonify({"error": "A network error occurred", "details": str(e)}), 500
    except ValueError as e:
        return jsonify({"error": "Invalid input data", "details": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500

if __name__ == "__main__":
    import os
    os.environ['FLASK_SKIP_DOTENV'] = '1'
    app.run(debug=True)
