from fastapi import APIRouter, Depends
from ..database import SessionLocal
from ..models import FAQ
from ..schemas import FAQCreate

from fastapi import Depends, HTTPException
from jose import jwt
from ..config import SECRET_KEY, ALGORITHM
from ..models import User
from ..database import SessionLocal

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

def get_current_user(token: str):
    db = SessionLocal()

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user = db.query(User).filter(User.id == payload["user_id"]).first()
        return user
    except:
        raise HTTPException(status_code=401, detail="Invalid token")
    
@router.post("/faq")
def create_faq(data: FAQCreate, token: str):
    user = get_current_user(token)