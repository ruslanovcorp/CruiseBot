from fastapi import FastAPI
from .database import Base, engine
from .routers import webhook, admin, auth

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(webhook.router)
app.include_router(admin.router)
app.include_router(auth.router)
    