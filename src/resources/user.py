import os
from datetime import timedelta
from passlib.hash import pbkdf2_sha256

from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import create_access_token, get_jwt, jwt_required

from blocklist import jwt_redis_blocklist
from models import UserModel, UserRoleModel, RideModel
from schemas import UserSchema, UserLoginSchema, UserRoleSchema


blp = Blueprint("Users", "users",
                description="Operation on users, be they drivers or passagens.")


@blp.route("/")
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    @blp.response(201, UserSchema)
    def post(self, user_data):
        if UserModel.find_by_email(user_data['email']):
            abort(409, message="An user with that email already exists.")

        if not UserRoleModel.find_by_id(user_data["role_id"]):
            abort(404, message="Role not found")

        user = UserModel(**user_data)

        user.save_to_db()

        # return {"message": "User created succefully."}, 201
        return user


@blp.route('/')
class UserList(MethodView):
    @jwt_required()
    @blp.response(200, UserSchema(many=True))
    def get(self):
        return UserModel.query.all()


@blp.route('/<string:user_id>')
class User(MethodView):
    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user

    @jwt_required()
    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        user.delete_from_db()

        return {"message": "User deleted."}, 200


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


# TODO: Add schema
# TODO: Add test
@blp.route('/<string:user_id>/rides/<string:role_name>')
class UserRides(MethodView):
    # application may have more roles, like admin, support, so on. But only driver and passenger will have rides
    roles = ["user", "driver"]

    def get(self, user_id, role_name):
        if role_name not in UserRides.roles:
            abort(404, message="Invalid role")

        for role in UserRides.roles:
            if role_name == "user":
                rides = RideModel.find_rides_passenger(user_id)
            elif role_name == "driver":
                rides = RideModel.find_rides_driver(user_id)
            else:
                abort(501, message="Method not implemented for this role")

        if not rides:
            abort(404, message="Rides not found for this user id and role")

        return rides


@blp.route('/role/<string:role_id>')
class UserRole(MethodView):
    @blp.response(200, UserRoleSchema)
    def get(self, role_id):
        role = UserRoleModel.query.get_or_404(role_id)
        return role


@blp.route('/role')
class UserRoleList(MethodView):
    @blp.response(200, UserRoleSchema(many=True))
    def get(self):
        return UserRoleModel.query.all()


@blp.route('/role/register')
class UserRoleRegister(MethodView):
    @jwt_required()
    @blp.arguments(UserRoleSchema)
    @blp.response(201, UserRoleSchema)
    def post(self, user_role_data):
        if UserRoleModel.find_by_name(user_role_data['name']):
            abort(409, message="An user role with that name already exists.")

        role = UserRoleModel(**user_role_data)
        role.save_to_db()
        return role
