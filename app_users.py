import os
from dotenv import load_dotenv

from flask import Flask

from db import db

def create_app(db_url=None):
    app = Flask(__name__)
    load_dotenv()

    #All loading stuffs and configuration
    app.config["PROPAGATE_EXCEPTION"] = os.getenv("FLASK_PROPAGATE_EXCEPTION", False)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite///data.db")

    db.init_app(app)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=os.getenv("USERS_API_PORT"))