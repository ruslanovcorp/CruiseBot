from .models import FAQ

def find_faq_answer(message: str, db):
    faqs = db.query(FAQ).all()

    message_lower = message.lower()

    for faq in faqs:
        if faq.question.lower() in message_lower:
            return faq.answer

    return None