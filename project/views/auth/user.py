from flask import request
from flask_restx import Namespace, Resource

from project.container import user_service
from project.setup.api.models import user

api = Namespace('user')


@api.route('/')
class UserView(Resource):
    @api.response(404, 'Not Found')
    @api.marshal_with(user, code=200, description='OK')
    def get(self):
        """

        Получение данных авторизованного пользователя.

        """

        token = request.headers.environ.get('HTTP_AUTHORIZATION').replace('Bearer ', '')
        user = user_service.get_user_by_token(refresh_token=token), 200
        return user

    @api.response(404, 'Not Found')
    @api.marshal_with(user, code=200, description='OK')
    def patch(self):
        """

        Изминение данных авторизованного пользователя.

        """

        user_d = request.json
        token = request.headers.environ['HTTP_AUTHORIZATION'].replace('Bearer ', '')
        return user_service.update(token, user_d), 200


@api.route('/password/')
class UserPassUpdateViews(Resource):
    @api.response(404, 'Not Found')
    @api.marshal_with(user, code=200, description='OK')
    def put(self):
        """

        Изминение пароля авторизованного пользователя.

        """
        user_d = request.json
        token = request.headers.environ['HTTP_AUTHORIZATION'].replace('Bearer ', '')
        user_service.update_user_password(token, user_d)
        return user_service.update(token, user_d), 200
