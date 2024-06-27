from flask import Blueprint
from flask_restful import Api
from routers.userRouters import UserRouter, LoginRouter, RegisterRouter
from routers.emailRouters import emailRouter
api_bp = Blueprint('api', __name__)

api = Api(api_bp)

api.add_resource(UserRouter, '/users', '/users/<int:user_id>')
api.add_resource(LoginRouter, '/login', '/login/<int:user_id>')
api.add_resource(RegisterRouter, '/register', '/register/<int:user_id>')
api.add_resource(emailRouter, '/send_email')