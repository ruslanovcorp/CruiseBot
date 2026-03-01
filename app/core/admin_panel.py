from sqladmin import ModelView
from .models import User, Company, FAQ


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.email, User.company_id]


class CompanyAdmin(ModelView, model=Company):
    column_list = [Company.id, Company.name]


class FAQAdmin(ModelView, model=FAQ):
    column_list = [FAQ.id, FAQ.question, FAQ.answer, FAQ.company_id]