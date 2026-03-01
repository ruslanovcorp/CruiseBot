from fastapi import APIRouter, Request
from ..database import SessionLocal
from ..models import Company
from ..services.faq_service import find_faq_answer
from ..services.messaging_service import send_whatsapp

router = APIRouter()

@router.post("/webhook")
async def webhook(request: Request):
    data = await request.json()

    if data.get("object") == "whatsapp_business_account":
        db = SessionLocal()

        for entry in data["entry"]:
            for change in entry["changes"]:
                value = change["value"]

                phone_number_id = value["metadata"]["phone_number_id"]

                company = db.query(Company).filter(
                    Company.phone_number_id == phone_number_id
                ).first()

                if not company:
                    continue

                if "messages" in value:
                    msg = value["messages"][0]
                    phone = msg["from"]
                    text = msg["text"]["body"]

                    faq = find_faq_answer(text, db, company.id)

                    reply = faq.answer if faq else "Здравствуйте! Напишите ваш вопрос."

                    send_whatsapp(company, phone, reply)

        db.close()

    return {"status": "ok"}