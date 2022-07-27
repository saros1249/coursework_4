from flask import request
from flask_restx import Namespace, Resource
from project.container import user_service, user_dao
from project.services.decorators import auth_required
from project.setup.api.models import user


api = Namespace('auth')

@api.route('/register')
class RegisterView(Resource):
    @api.marshal_with(user, as_list=True, code=200, description='OK')
    def post(self):
        data_user = request.json
        if data_user.get('email') and data_user.get('password'):
            user_service.create(data_user.get('email'), data_user.get('password'))
            return user_service.get_by_email(data_user.get('email')), 201
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

    @api.response(404, 'Not Found')
    @api.marshal_with(user, code=200, description='OK')
    #@auth_required
    def put(self):
        data = request.json
        if data.get('access_token') and data.get('refresh_token'):
            return user_service.check_tokens(data.get('refresh_token')), 201
        else:
            return 'Введены не все данные', 400




