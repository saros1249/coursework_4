from flask_restx import Namespace

api = Namespace('user')

@api.route('/')
class UserView(Resource):
    schema = UserSchema(many=True)

    def get(self):
        return self.schema.dump(user_service.get_all()), 200

    def post(self):
        user = user_service.create(request.json)
        res = make_response('Новый пользователь добавлен', 201)
        res.headers['location'] = f'{user_ns.path}/{user.id}'
        return res


@api.route('/<int:uid>')
class UserView(Resource):
    schema = UserSchema

    def put(self, uid: int):
        user = self.schema.dump(user_service.update(uid, request.json))
        return f'Запись с ID{uid} изменена на {user}.', 200

    def delete(self, uid: int):
        user_service.delete(uid)
        return 204