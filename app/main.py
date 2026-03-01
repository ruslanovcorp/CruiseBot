from fastapi import FastAPI, Request
import os
import requests
from dotenv import load_dotenv
from sqlalchemy.orm import Session

from .database import engine, SessionLocal, Base
from .models import FAQ

Base.metadata.create_all(bind=engine)

load_dotenv()

app = FastAPI()

@app.get("/")
def root():
    return {"status": "ok"}

@app.get("/privacy")
def privacy():
    return {"message": "Privacy Policy"}

@app.get("/data-deletion")
def delete():
    return {"message": "Data deletion instructions"}
    

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
INSTAGRAM_TOKEN = os.getenv("INSTAGRAM_TOKEN")

# =========================
# DATABASE SEARCH FUNCTION
# =========================

def get_faq_answer(user_text: str):
    db: Session = SessionLocal()
    try:
        faqs = db.query(FAQ).all()
        for faq in faqs:
            if faq.question.lower() in user_text.lower():
                return faq.answer
        return None
    finally:
        db.close()

# =========================
# WEBHOOK VERIFICATION
# =========================

@app.get("/webhook")
async def verify_webhook(request: Request):
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return int(challenge)

    return {"status": "verification failed"}

# =========================
# WEBHOOK RECEIVER
# =========================

@app.post("/webhook")
async def receive_webhook(request: Request):
    data = await request.json()
    print("INCOMING:", data)

    if "object" in data:

        # =========================
        # WHATSAPP
        # =========================
        if data["object"] == "whatsapp_business_account":
            for entry in data["entry"]:
                for change in entry.get("changes", []):
                    value = change.get("value", {})

                    if "messages" in value:
                        msg = value["messages"][0]
                        phone = msg["from"]
                        text = msg["text"]["body"]

                        reply = generate_response(text)
                        send_whatsapp(phone, reply)

        # =========================
        # INSTAGRAM
        # =========================
        if data["object"] == "instagram":
            for entry in data.get("entry", []):
                for messaging_event in entry.get("messaging", []):

                    # Обрабатываем ТОЛЬКО обычные сообщения
                    if "message" in messaging_event and "text" in messaging_event["message"]:

                        sender_id = messaging_event["sender"]["id"]
                        text = messaging_event["message"]["text"]

                        print("IG TEXT:", text)

                        reply = generate_response(text)
                        print("IG REPLY:", reply)

                        send_instagram(sender_id, reply)

    return {"status": "ok"}
# =========================
# RESPONSE GENERATOR
# =========================

def generate_response(text):
    db_answer = get_faq_answer(text)

    if db_answer:
        return db_answer

    return "Здравствуйте! Напишите ваш вопрос, и мы ответим в ближайшее время."

# =========================
# SEND WHATSAPP
# =========================

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
    print("WHATSAPP STATUS:", response.status_code, response.text)

# =========================
# SEND INSTAGRAM1
# =========================

def send_instagram(user_id, message):
    url = f"https://graph.facebook.com/v19.0/{os.getenv('IG_BUSINESS_ID')}/messages"

    headers = {
        "Authorization": f"Bearer {INSTAGRAM_TOKEN}",
        "Content-Type": "application/json"
    }

    data = {
        "messaging_product": "instagram",
        "recipient": {"id": user_id},
        "message": {"text": message}
    }

    response = requests.post(url, headers=headers, json=data)
    print("INSTAGRAM STATUS:", response.status_code, response.text)