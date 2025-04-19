from db import db
from enum import Enum
from sqlalchemy.types import Enum as SQLAlchemyEnum

class AccountType(Enum):
    ADMIN = 'admin'
    USER = 'user'


class UserModel(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(127), nullable=False, unique=True)
    password = db.Column(db.String(127), nullable=False)
    account_type = db.Column(SQLAlchemyEnum(AccountType), 
                           nullable=False)
    applications = db.relationship('ApplicationModel', back_populates='approver', lazy='dynamic')

    def is_admin(self):
        return self.account_type == AccountType.ADMIN
    
    def is_user(self):
        return self.account_type == AccountType.USER