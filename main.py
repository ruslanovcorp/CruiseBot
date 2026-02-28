from fastapi import FastAPI, Request
import os
import requests
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")

@app.get("/webhook")
async def verify_webhook(request: Request):
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return int(challenge)

    return {"status": "ok"}

@app.post("/webhook")
async def receive_webhook(request: Request):
    data = await request.json()
    print("INCOMING:", data)

    if "entry" in data:
        for entry in data["entry"]:
            for change in entry.get("changes", []):
                value = change.get("value", {})

                if "messages" in value:
                    msg = value["messages"][0]
                    phone = msg["from"]
                    text = msg["text"]["body"]

                    reply = generate_response(text)
                    send_whatsapp(phone, reply)

    return {"status": "ok"}

def generate_response(text):
    text = text.lower()

    if "цена" in text:
        return "Стоимость круиза начинается от 1200$."
    if "маршрут" in text:
        return "Доступны Карибы, Средиземное море и Азия."

    return "Здравствуйте! Вас интересует цена или маршрут?"

def send_whatsapp(phone, message):
    url = f"https://graph.facebook.com/v19.0/{PHONE_NUMBER_ID}/messages"

    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }

    data = {
        "messaging_product": "whatsapp",
        "to": phone,
        "type": "text",
        "text": {"body": message}
    }

    response = requests.post(url, headers=headers, json=data)
    print("SEND STATUS:", response.status_code, response.text)