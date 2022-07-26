from flask import request
from flask_restx import Namespace, Resource
from project.container import user_service
from project.setup.api.models import user
from project.tools import security

api = Namespace('auth')

@api.route('/register')
class RegisterView(Resource):
    @api.marshal_with(user, as_list=True, code=200, description='OK')
    def post(self):
        data_user = request.json
        if data_user.get('email') and data_user.get('password'):
            return user_service.create(data_user.get('email'), data_user.get('password')), 201
        else:
            return 'Введены не все данные', 400

@api.route('/login')
class LoginView(Resource):
    @api.response(404, 'Not Found')
    @api.marshal_with(user, code=200, description='OK')
    def post(self):
        data_user = request.json
        if data_user.get('email') and data_user.get('password'):
            return user_service.check(data_user.get('email'), data_user.get('password')), 201
        else:
            return 'Введены не все данные', 400

    def put(self):
        req_json = request.json
        ref_token = req_json.get('refresh_token')
        if not ref_token:
            return 'Не задан токен', 400

        tokens = security.approve_refresh_token(ref_token)
        if tokens:
            return tokens
        else:
            return 'Ошибка запроса', 400



