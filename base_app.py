import os
from dotenv import load_dotenv
from datetime import timedelta

from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_smorest import Api, Blueprint

from db import db
from blocklist import jwt_redis_blocklist


def create_app(api_name, db_url=None, blueprints=None):
    load_dotenv()

    def create_subapp(db_url, api_name):
        app = Flask(__name__)

        # All loading stuffs and configuration
        app.config["PROPAGATE_EXCEPTION"] = os.getenv(
            "FLASK_PROPAGATE_EXCEPTION", False)
        app.config["SQLALCHEMY_DATABASE_URI"] = db_url if db_url else os.getenv(
            "DATABASE_URL", "sqlite///data.db")

        app.config["API_TITLE"] = "{} - {}".format(
            os.getenv("API_TITLE", ""), api_name)
        app.config["API_VERSION"] = "v1"
        app.config["OPENAPI_VERSION"] = "3.0.3"
        app.config["OPENAPI_URL_PREFIX"] = "/"
        app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
        app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
        app.config["DEBUG"] = True

        db.init_app(app)
        api = Api(app)

        app.config['JWT_SECRET_KEY'] = os.getenv(
            "JWT_SECRET_KEY", False)
        app.config['ACCESS_EXPIRES'] = timedelta(hours=int(os.getenv(
            "ACCESS_EXPIRES_HOURS", 1)))
        jwt = JWTManager(app)

        # Callback function to check if a JWT exists in the redis blocklist
        @jwt.token_in_blocklist_loader
        def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
            jti = jwt_payload["jti"]
            token_in_redis = jwt_redis_blocklist.get(jti)
            return token_in_redis is not None

        @jwt.revoked_token_loader
        def revoked_token_callback(jwt_header, jwt_payload):
            return (
                jsonify(
                    {
                        "description": "The token has been revoked.",
                        "error": "token_revoked"
                    }
                ),401
            )
        
        @jwt.expired_token_loader
        def expired_token_callback(jwt_header, jwt_payload):
            return(
                jsonify(
                    {
                        "message":"The token has expired.",
                        "error":"token_expired"
                    }
                ),401
            )

        return app, api
    
    app, api = create_subapp(db_url, api_name)
    if blueprints:
        for blp in blueprints:
            if isinstance(blp, Blueprint):
                api.register_blueprint(blp)
            else:
                print("{} is not an instance of Blueprint".format(blp))

    return app