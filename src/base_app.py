import os
import functools
from dotenv import load_dotenv
from datetime import timedelta

from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_smorest import Api, Blueprint
from flask_migrate import Migrate

from db import db, verify_init_sql
from models import UserRoleModel
from models.user import db as db2
from blocklist import jwt_redis_blocklist

#Set it with powershell to run this command, then remove it
# $env:ALEMBIC_MIGRATE="1"
# $env:ALEMBIC_MIGRATE="-1"
# on the same terminal session, run flask --app base_app.py db init
# flask --app base_app.py db migrate
# blueprints are needed so the program can create the right tables
if os.getenv("ALEMBIC_MIGRATE") == "1":
    from resources import RideBlueprint, UserBlueprint, VehicleBlueprint, BaseBlueprint
    blueprints = [RideBlueprint, UserBlueprint, VehicleBlueprint, BaseBlueprint]
    api_name=""
else:
    blueprints=None

load_dotenv()

def declare_roles(func):
    @functools.wraps(func)
    def wrapper_decorator(*args, **kwargs):
        app = func(*args, **kwargs)
        if "Users" in kwargs.get('api_name','') and not kwargs.get('test_mode', False):
            with app.app_context():
                role_passanger = {"name": "passanger"}
                role_admin = {"name": "driver"}
                if not UserRoleModel.find_by_name(**role_passanger):
                    db.session.add(UserRoleModel(**role_passanger))
                if not UserRoleModel.find_by_name(**role_admin):
                    db.session.add(UserRoleModel(**role_admin))
                db.session.commit()
        return app
    return wrapper_decorator

@declare_roles
def create_app(api_name, db_url=None, blueprints=blueprints, test_mode=False):
    def create_subapp(db_url, api_name):
        app = Flask(__name__)

        # All loading stuffs and configuration
        app.config["PROPAGATE_EXCEPTION"] = os.getenv(
            "FLASK_PROPAGATE_EXCEPTION", False)

        POSTGRES_USER = os.getenv(
            "POSTGRES_USER")
        POSTGRES_PASSWORD = os.getenv(
            "POSTGRES_PASSWORD")
        POSTGRES_DB = os.getenv(
            "POSTGRES_DB")

        #NOTE: database = same name as docker-compose.yml service for postgres
        if os.getenv("DOCKER_CONTAINER", "-1") == "1":
            db_ip = "database"
        else:
            db_ip = "127.0.0.1"

        POSTGRES_HOST = os.getenv("POSTGRES_PORT")
        db_host = POSTGRES_HOST if POSTGRES_HOST else db_ip
        DATABASE_URL = "postgresql://{}:{}@{}:5432/{}".format(
            POSTGRES_USER, POSTGRES_PASSWORD, db_host, POSTGRES_DB)
        app.config["SQLALCHEMY_DATABASE_URI"] = db_url if db_url else DATABASE_URL

        app.config["API_TITLE"] = "{} - {}".format(
            os.getenv("API_TITLE", ""), api_name)
        app.config["API_VERSION"] = "v1"
        app.config["OPENAPI_VERSION"] = "3.0.3"
        app.config["OPENAPI_URL_PREFIX"] = "/"
        app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
        app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
        app.config["DEBUG"] = True

        db.init_app(app)
        migrate = Migrate(app, db, directory=os.path.join("database","migrations"))
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
                ), 401
            )

        @jwt.expired_token_loader
        def expired_token_callback(jwt_header, jwt_payload):
            return (
                jsonify(
                    {
                        "message": "The token has expired.",
                        "error": "token_expired"
                    }
                ), 401
            )

        return app, api

    app, api = create_subapp(db_url, api_name)
    if blueprints:
        for blp in blueprints:
            if isinstance(blp, Blueprint):
                api.register_blueprint(blp)
            else:
                print("{} is not an instance of Blueprint".format(blp))

    with app.app_context():
        if os.getenv("UNITTEST", "-1") != "1":
            verify_init_sql()

    return app