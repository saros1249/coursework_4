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
        token = request.headers.environ.get('HTTP_AUTHORIZATION').replace('Bearer ', '')
        return user_service.get_user_by_token(refresh_token=token), 200


    @api.response(404, 'Not Found')
    @api.marshal_with(user, code=200, description='OK')
    def patch(self):
        user_d = request.json
        token = request.headers.environ['HTTP_AUTHORIZATION'].replace('Bearer ', '')
        return user_service.update(token, user_d)

@api.route('/password/')
class UserPassUpdateViews(Resource):
    @api.response(404, 'Not Found')
    @api.marshal_with(user, code=200, description='OK')
    def put(self):
        user_d = request.json
        token = request.headers.environ['HTTP_AUTHORIZATION'].replace('Bearer ', '')
        user_by_token = user_service.get_user_by_token(refresh_token=token)
        return user_service.update_user_password(user_by_token, user_d)

