from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..models import User, Company
from passlib.context import CryptContext
from jose import jwt
from ..config import SECRET_KEY, ALGORITHM
from pydantic import BaseModel

router = APIRouter(prefix="/auth")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class RegisterSchema(BaseModel):
    company_name: str
    email: str
    password: str

class LoginSchema(BaseModel):
    email: str
    password: str


def create_access_token(data: dict):
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)


@router.post("/register")
def register(data: RegisterSchema):
    db: Session = SessionLocal()

    hashed_password = pwd_context.hash(data.password)

    company = Company(name=data.company_name)
    db.add(company)
    db.commit()
    db.refresh(company)

    user = User(
        email=data.email,
        password=hashed_password,
        company_id=company.id
    )

    db.add(user)
    db.commit()

    token = create_access_token({"user_id": user.id})

    return {"access_token": token}


@router.post("/login")
def login(data: LoginSchema):
    db: Session = SessionLocal()

    user = db.query(User).filter(User.email == data.email).first()

    if not user or not pwd_context.verify(data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"user_id": user.id})

    return {"access_token": token}