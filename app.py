from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import requests
import os

app = Flask(__name__)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def ai_reply(message):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "mixtral-8x7b-32768",
        "messages": [
            {"role": "system", "content": "You are a friendly human-like assistant for car spare parts sales."},
            {"role": "user", "content": message}
        ]
    }

    response = requests.post(url, json=data, headers=headers).json()
    return response["choices"][0]["message"]["content"]

@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    incoming = request.form.get("Body")
    reply_text = ai_reply(incoming)

    r = MessagingResponse()
    r.message(reply_text)
    return str(r)

@app.route("/")
def home():
    return "Bot is running with Groq!"
