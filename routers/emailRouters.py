from flask import request
from flask_restful import Resource
from controllers.emailControllers import emailControllers

class emailRouter(Resource):

    # set content type to json
    @staticmethod
    def post():
        result = emailControllers.send_email(request)
        return result
