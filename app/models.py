from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    whatsapp_token = Column(Text)
    phone_number_id = Column(String)
    instagram_token = Column(Text)
    ig_business_id = Column(String)

    faqs = relationship("FAQ", back_populates="company")


class FAQ(Base):
    __tablename__ = "faqs"

    id = Column(Integer, primary_key=True)
    question = Column(String, nullable=False)
    answer = Column(Text, nullable=False)

    company_id = Column(Integer, ForeignKey("companies.id"))
    company = relationship("Company", back_populates="faqs")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    is_admin = Column(Boolean, default=True)

    company_id = Column(Integer, ForeignKey("companies.id"))