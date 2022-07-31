

from flask import request
from flask_restx import Namespace, Resource

from project.container import movie_service
from project.services import favorites_service
from project.setup.api.models import favorites_genres

api = Namespace('favorites')


@api.route('favorites/<int:user_id>/')
class FavoritesView(Resource):
    @api.response(404, 'Not Found')
    @api.marshal_with(favorites_genres, code=200, description='OK')
    def get(self, user_id: int):
        """
        Get movie by id.
        """
        return favorites_service.get_item(user_id)

    @api.response(404, 'Not Found')
    @api.marshal_with(favorites_genres, code=200, description='OK')
    def post(self):
        pass


    @api.response(404, 'Not Found')
    @api.marshal_with(favorites_genres, code=200, description='OK')
    def delete(self):
        pass



