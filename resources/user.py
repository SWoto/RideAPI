from passlib.hash import pbkdf2_sha256

from flask.views import MethodView
from flask_smorest import Blueprint, abort

from db import db
from models import UserModel
from schemas import UserSchema

blp = Blueprint("Users", "users",
                description="Operation on users, be they drivers or passagens.")


@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        if UserModel.query.filter(UserModel.email == user_data["email"]).first():
            abort(409, message="An user with that email already exists.")

        user = UserModel(username=user_data['username'],
                         email=user_data['email'],
                         password=pbkdf2_sha256.hash(user_data['password']),
                         role=user_data['role'])

        db.session.add(user)
        db.session.commit()

        return {"message": "user created succefully."}, 201