import os
from dotenv import load_dotenv

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_smorest import Api


from db import db
from resources.user import blp as UserBlueprint

API_NAME = "Users MS."

def create_app(db_url=None):
    app = Flask(__name__)
    load_dotenv()

    # All loading stuffs and configuration
    app.config["PROPAGATE_EXCEPTION"] = os.getenv(
        "FLASK_PROPAGATE_EXCEPTION", False)
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url if db_url else os.getenv(
        "DATABASE_URL", "sqlite///data.db")

    app.config["API_TITLE"] = "{} - {}".format(
        os.getenv("API_TITLE", ""), API_NAME)
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
    jwt = JWTManager(app)

    api.register_blueprint(UserBlueprint)

    return app


if __name__ == "__main__":
    app = create_app()

    if app.config['DEBUG']:
        with app.app_context():
            @app.before_first_request
            def create_tables():
                db.create_all()

    app.run(host="0.0.0.0", port=os.getenv("USERS_API_PORT"))
