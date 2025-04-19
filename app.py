import os
import secrets

from flask import Flask, jsonify
from flask_smorest import Api
from flask_migrate import Migrate
from db import db

import models
from resources.application import blp as application_blp
from resources.user import blp as user_blp, register_jwt_handlers

from flask_jwt_extended import JWTManager

def create_app(db_url=None):
    app = Flask(__name__)
    app.config['SECRET_KEY'] = str(secrets.SystemRandom().getrandbits(128))

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config[
        "OPENAPI_SWAGGER_UI_URL"
    ] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    

    app.config['UPLOAD_FOLDER'] = 'media'
    app.config['MAX_CONTENT_LENGTH'] = 10*1024*1024  #10MB
    
    db.init_app(app)
    migrate = Migrate(app, db)
    api = Api(app)

    app.config["JWT_SECRET_KEY"] = str(secrets.SystemRandom().getrandbits(128))
    jwt = JWTManager(app)
    register_jwt_handlers(jwt)


    api.register_blueprint(application_blp)
    api.register_blueprint(user_blp)

    return app

app = create_app()
