from marshmallow import Schema, fields, validate, validates, ValidationError
from datetime import date
from models.user import AccountType  # Import the enum

class ApplicationSchema(Schema):
    """
    Application Schema
    """
    id = fields.Int(dump_only=True)
    first_name = fields.Str(required=True, validate=validate.Length(max=127))
    last_name = fields.Str(required=True, validate=validate.Length(max=127))
    dob = fields.Date(required=True)
    email = fields.Str(required=True, validate=validate.Length(max=127))
    phone = fields.Str(required=True, validate=validate.Length(min=10, max=20))
    degree = fields.Str(required=True, validate=validate.Length(max=127))
    field_of_study = fields.Str(required=True, validate=validate.Length(max=127))
    institution = fields.Str(required=True, validate=validate.Length(max=127))
    cgpa = fields.Float(required=True, validate=validate.Range(min=0, max=10))
    transcript_filename = fields.Str(required=True, validate=validate.Length(max=255))
    id_proof_filename = fields.Str(required=True, validate=validate.Length(max=255))
    application_status = fields.Str(
        validate=validate.OneOf(['pending', 'approved', 'rejected']),
        default='pending'
    )
    approved_by = fields.Int(dump_only=True)


class UserSchema(Schema):
    """
    User Schema
    """
    id = fields.Int(dump_only=True)
    username = fields.Str(
        required=True, 
        validate=validate.Length(max=127)
    )
    password = fields.Str(
        load_only=True, 
        required=True, 
        validate=validate.Length(max=127)
    )
    account_type = fields.Enum(
        AccountType,
        by_value=True,
        required=True
    )