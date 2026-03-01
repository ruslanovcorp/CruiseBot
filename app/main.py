from fastapi import FastAPI
from .database import Base, engine
from .routers import webhook, admin, auth

from sqladmin import Admin
from .database import engine

from .admin_panel import UserAdmin, CompanyAdmin, FAQAdmin

Base.metadata.create_all(bind=engine)

app = FastAPI()

admin = Admin(app, engine)

app.include_router(webhook.router)
app.include_router(admin.router)
app.include_router(auth.router)

admin.add_view(UserAdmin)
admin.add_view(CompanyAdmin)
admin.add_view(FAQAdmin)
    