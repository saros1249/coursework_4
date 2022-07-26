from flask import request
from flask_restx import Namespace, Resource

from project.container import user_service
from project.setup.api.models import user

api = Namespace('user')

@api.route('/')
class UserView(Resource):
    @api.response(404, 'Not Found')
    @api.marshal_with(user, code=200, description='OK')
    def get(self, email):
        return user_service.get_one(email), 200

    def patch(self, email):
        self.user_service.update(email, request.json)
        return f'Запись пользователя {email} изменена.', 200

    def put(self, email, password, new_password):
        user_service.update(email, password, new_password)
        return 204

