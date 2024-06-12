from flask import request
from flask_restful import Resource
from controllers.userControllers import UserControllers


class UserRouter(Resource):
    @staticmethod
    def get(user_id=None):
        if user_id:
            return UserControllers.get_user_by_id(user_id)
        return UserControllers.get_all_users(request)

    # set content type to json
    @staticmethod
    def post():
        result = UserControllers.create_user(request)
        return result

    @staticmethod
    def put(user_id):
        return UserControllers.update_user(request, user_id)

    @staticmethod
    def delete():
        return UserControllers.delete_user(request)


class LoginRouter(Resource):
    @staticmethod
    def post():
        return UserControllers.login_user(request)


class RegisterRouter(Resource):
    @staticmethod
    def post():
        return UserControllers.register_user(request)

class LogoutRouter(Resource):
    @staticmethod
    def post():
        return UserControllers.logout_user(request)
