from fastapi import FastAPI
from .database import Base, engine
from .routers import webhook, admin, auth

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://cruise-admin.vercel.app",  # потом пригодится
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(webhook.router)
app.include_router(admin.router)
app.include_router(auth.router)
    