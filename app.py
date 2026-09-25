from flask import Flask, request, jsonify
from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

# Get API key from .env
api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

# Chat memory
chat_history = []


# Clear chat memory
@app.route("/clear", methods=["POST"])
def clear_chat():
    chat_history.clear()

    return jsonify({
        "message": "Chat memory cleared!"
    })


# Home
@app.route("/")
def home():
    return "Farhan AI Backend is running!"


# Chat
@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json()
    user_message = data.get("message", "")

    # Save user message
    chat_history.append({
        "role": "user",
        "text": user_message
    })

    # Create conversation for Gemini
    conversation = ""

    for message in chat_history:
        conversation += message["role"] + ": " + message["text"] + "\n"

    # Send to Gemini
    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=conversation
    )

    ai_reply = response.text

    # Save AI reply
    chat_history.append({
        "role": "assistant",
        "text": ai_reply
    })

    return jsonify({
        "reply": ai_reply
    })


# Run Flask
if __name__ == "__main__":
    app.run(debug=True)