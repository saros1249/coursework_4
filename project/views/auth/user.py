from flask import request, make_response
from flask_restx import Namespace, Resource

from project.container import user_service

api = Namespace('user')

@api.route('/')
class UserView(Resource):

    def get(self, email):
        return user_service.get_one(email), 200

    def patch(self, uid: int):
        user = self.user_service.update(uid, request.json)
        return f'Запись с ID{uid} изменена на {user}.', 200


@api.route('/<int:uid>')
class UserView(Resource):

    def put(self, email, password, new_password):
        user_service.delete(uid)
        return 204