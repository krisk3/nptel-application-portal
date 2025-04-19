from flask import jsonify
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash

from models.user import UserModel, AccountType
from schemas import UserSchema
from db import db

blp = Blueprint("Users", "users", description="Operations on users")

class LoginSchema(UserSchema):
    class Meta:
        fields = ("username", "password")

def register_jwt_handlers(jwt: JWTManager):
    
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({"message": "The token has expired.", "error": "token_expired"}),
            401,
        )

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify(
                {"message": "Signature verification failed.", "error": "invalid_token"}
            ),
            401,
        )

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify(
                {
                    "description": "Request does not contain an access token.",
                    "error": "authorization_required",
                }
            ),
            401,
        )

