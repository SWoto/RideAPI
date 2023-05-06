from passlib.hash import pbkdf2_sha256
import uuid

from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import create_access_token

from db import db
from models import UserModel
from schemas import UserSchema

blp = Blueprint("Users", "users",
                description="Operation on users, be they drivers or passagens.")


@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    @blp.response(201, UserSchema)
    def post(self, user_data):
        if UserModel.query.filter(UserModel.email == user_data["email"]).first():
            abort(409, message="An user with that email already exists.")

        user = UserModel(id=uuid.uuid4().hex,
                         username=user_data['username'],
                         email=user_data['email'],
                         password=pbkdf2_sha256.hash(user_data['password']),
                         role=user_data['role'])

        user.save_to_db()

        #return {"message": "User created succefully."}, 201
        return user


@blp.route('/login')
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        user = UserModel.find_by_email(user_data['email'])
        if user and pbkdf2_sha256.verify(user_data['password'], user.password):
            access_token = create_access_token(identity=user.id, fresh=True)
            return {'access_token':access_token}
        
        abort(401, message='Invalid credentials.')


@blp.route('/logout')
class UserLogout(MethodView):
    @blp.arguments(UserSchema)
    def post(self):
        pass



@blp.route('/user/<string:user_id>')
class User(MethodView):
    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            abort(404, message='There is no user with requested id')

        return user

    def delete(self, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            abort(404, message='There is no user with requested id')

        user.delete_from_db()
        return {"message": "User deleted"}, 200
