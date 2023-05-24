import os
from datetime import timedelta
from passlib.hash import pbkdf2_sha256

from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import create_access_token, get_jwt, jwt_required

from blocklist import jwt_redis_blocklist
from models import UserModel, UserRoleModel
from schemas import UserSchema, UserLoginSchema, UserRoleSchema


blp = Blueprint("Users", "users",
                description="Operation on users, be they drivers or passagens.")


#TODO: Add role valdiation (post_load decorator?)
#TODO: Add vehicle validation (post_load decorator?)
@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    @blp.response(201, UserSchema)
    def post(self, user_data):
        if UserModel.find_by_email(user_data['email']):
            abort(409, message="An user with that email already exists.")

        user = UserModel(**user_data)

        user.save_to_db()

        # return {"message": "User created succefully."}, 201
        return user


@blp.route('/login')
class UserLogin(MethodView):
    @blp.arguments(UserLoginSchema)
    def post(self, user_data):
        user = UserModel.find_by_email(user_data['email'])
        if user and pbkdf2_sha256.verify(user_data['password'], user.password):
            access_token = create_access_token(identity=user.id, fresh=True)
            return {'access_token': access_token}

        abort(401, message='Invalid credentials.')


@blp.route('/logout')
class UserLogout(MethodView):
    @jwt_required()
    def delete(self):
        access_expires = timedelta(hours=int(os.getenv(
            "ACCESS_EXPIRES_HOURS", 1)))
        jti = get_jwt()['jti']
        jwt_redis_blocklist.set(jti, "", ex=access_expires)
        return {'message': 'Successfully logged out.'}


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


@blp.route('/user')
class UserList(MethodView):
    @jwt_required()
    @blp.response(200, UserSchema(many=True))
    def get(self):
        return UserModel.query.all()


@blp.route('/user/role/<string:role_id>')
class UserRole(MethodView):
    @blp.response(200, UserRoleSchema)
    def get(self, role_id):
        role = UserRoleModel.query.get_or_404(role_id)
        return role


@blp.route('/user/role')
class UserRoleList(MethodView):
    @blp.response(200, UserRoleSchema(many=True))
    def get(self):
        return UserRoleModel.query.all()

#TODO: Add test
@blp.route('/user/role/register')
class UserRoleRegister(MethodView):
    @blp.arguments(UserRoleSchema)
    @blp.response(201, UserRoleSchema)
    def post(self, user_role_data):
        if UserRoleModel.find_by_name(user_role_data['name']):
            abort(409, message="An user role with that name already exists.")
        
        role = UserRoleModel(**user_role_data)
        role.save_to_db()
        return role