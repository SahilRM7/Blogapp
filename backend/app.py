from flask import Flask, request, jsonify, send_from_directory
import requests
import os

app = Flask(__name__, static_folder="../frontend", static_url_path="")

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
API_URL = "https://openrouter.ai/api/v1/chat/completions"

@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/<path:path>")
def serve_static(path):
    return send_from_directory(app.static_folder, path)

@app.route("/generate-blog", methods=["POST"])
def generate_blog():
    prompt = request.json.get("prompt", "").strip()
    if not prompt:
        return jsonify({"error": "Prompt cannot be empty"}), 400

    full_prompt = f"Write a detailed, well-structured blog of exact 1000 words on: {prompt}"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "deepseek/deepseek-r1:free",  # or deepseek-r1t2-chimera:free
        "messages": [{"role": "user", "content": full_prompt}]
    }

    resp = requests.post(API_URL, json=payload, headers=headers)
    if resp.status_code != 200:
        print("API response:", resp.text)
        return jsonify({"error": "Model call failed", "details": resp.text}), 500

    data = resp.json()
    content = data["choices"][0]["message"]["content"] if "choices" in data else str(data)
    return jsonify({"blog": content})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

