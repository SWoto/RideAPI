from passlib.hash import pbkdf2_sha256
import uuid
from datetime import timedelta
import os

from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import create_access_token, get_jwt, jwt_required

from db import db
from models import UserModel
from schemas import UserSchema
from blocklist import jwt_redis_blocklist

blp = Blueprint("Users", "users",
                description="Operation on users, be they drivers or passagens.")


@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    @blp.response(201, UserSchema)
    def post(self, user_data):
        if UserModel.find_by_email(user_data['email']):
            abort(409, message="An user with that email already exists.")

        user = UserModel(**user_data)

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
    @jwt_required()
    def delete(self):
        access_expires =  timedelta(hours=int(os.getenv(
        "ACCESS_EXPIRES_HOURS", 1)))
        jti = get_jwt()['jti']  
        jwt_redis_blocklist.set(jti, "", ex=access_expires)
        return {'message':'Successfully logged out.'}


@blp.route('/user/<string:user_id>')
class User(MethodView):
    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user

    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        user.delete_from_db()
        
        return {"message": "User deleted."}, 200

#TODO: Add test
@blp.route('/user')
class UserList(MethodView):
    @jwt_required()
    @blp.response(200, UserSchema(many=True))
    def get(self):
        return UserModel.query.all()
