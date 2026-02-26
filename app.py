from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import requests

app = Flask(__name__)

OPENAI_API_KEY = "YOUR_OPENAI_API_KEY"

def ai_reply(message):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {"Authorization": f"Bearer {OPENAI_API_KEY}"}

    data = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "You are a friendly human-like sales agent for car spare parts."},
            {"role": "user", "content": message}
        ]
    }

    response = requests.post(url, json=data, headers=headers)
    return response.json()["choices"][0]["message"]["content"]


@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    incoming_msg = request.form.get("Body")
    resp = MessagingResponse()
    reply = ai_reply(incoming_msg)
    resp.message(reply)
    return str(resp)


@app.route("/", methods=["GET"])
def home():
    return "Bot is running!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
