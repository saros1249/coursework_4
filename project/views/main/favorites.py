

from flask import request, jsonify
from flask_restx import Namespace, Resource

from project.container import movie_service, favorites_service
from project.setup.api.models import favorites

api = Namespace('favorites')


@api.route('/movies/')
class FavoritesView(Resource):
    @api.response(404, 'Not Found')
    @api.marshal_with(favorites, code=200, description='OK')
    def get(self):
        token = request.headers.environ.get('HTTP_AUTHORIZATION').replace('Bearer ', '')
        fav_list = favorites_service.get_all_favorites(token)
        print(fav_list)
        return jsonify(fav_list)

@api.route('/movies/<int:movie_id>/')
class FavoriteView(Resource):
    @api.response(404, 'Not Found')
    @api.marshal_with(favorites, code=200, description='OK')
    def post(self, movie_id):
        token = request.headers.environ.get('HTTP_AUTHORIZATION').replace('Bearer ', '')
        return favorites_service.update(movie_id, token)


    @api.response(404, 'Not Found')
    @api.marshal_with(favorites, code=200, description='OK')
    def delete(self, movie_id):
        token = request.headers.environ.get('HTTP_AUTHORIZATION').replace('Bearer ', '')
        return favorites_service.delete(movie_id, token)


