from flask import request, make_response
from flask_restx import Namespace, Resource

from project.container import auth_service, user_service

api = Namespace('auth')

@api.route('/register')
class AuthView(Resource):
    def post(self):
        user = user_service.create(request.json)
        res = make_response('Новый пользователь добавлен', 201)
        res.headers['location'] = f'{api.path}/{user.id}'
        return res

@api.route('/login')
class AuthView(Resource):
    def post(self):
        req_json = request.json
        email = req_json.get('email')
        password = req_json.get('password')
        if not email or password:
            return 'Не введены данные: имя пользователя и/или пароль.', 400

        tokens = auth_service.generate_tokens(email, password)
        if tokens:
            return tokens
        else:
            return 'Ошибка запроса', 400

@api.route('/login')
class AuthView(Resource):

    def put(self):
        req_json = request.json
        ref_token = req_json.get('refresh_token')
        if not ref_token:
            return 'Не задан токен', 400

        tokens = auth_service.approve_refresh_token(ref_token)
        if tokens:
            return tokens
        else:
            return 'Ошибка запроса', 400
