from fastapi import APIRouter, Depends
from ..database import SessionLocal
from ..models import FAQ
from ..schemas import FAQCreate

router = APIRouter(prefix="/admin")

@router.post("/faq")
def create_faq(data: FAQCreate):
    db = SessionLocal()
    faq = FAQ(question=data.question, answer=data.answer, company_id=1)
    db.add(faq)
    db.commit()
    return {"status": "created"}

@router.get("/faq")
def get_faqs():
    db = SessionLocal()
    return db.query(FAQ).all()