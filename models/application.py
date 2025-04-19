from db import db
from enum import Enum
from sqlalchemy.types import Enum as SQLAlchemyEnum
class ApplicationStatus(Enum):
    PENDING = 'pending'
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'

class ApplicationModel(db.Model):
    __tablename__ = 'application'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(127), nullable=False)
    last_name = db.Column(db.String(127), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    email = db.Column(db.String(127), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    degree = db.Column(db.String(127), nullable=False)
    field_of_study = db.Column(db.String(127), nullable=False)
    institution = db.Column(db.String(127), nullable=False)
    cgpa = db.Column(db.Float, nullable=False)
    transcript_filename = db.Column(db.String(255), nullable=False)
    id_proof_filename = db.Column(db.String(255), nullable=False)
    application_status = db.Column(SQLAlchemyEnum(ApplicationStatus), nullable=False, default=ApplicationStatus.PENDING)
    
    approved_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    approver = db.relationship('UserModel', back_populates='applications')