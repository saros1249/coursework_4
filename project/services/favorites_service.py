from flask import jsonify

from project.dao.favorites_dao import FavoritesDAO
from project.services import UserService


class FavoritesService:
    def __init__(self, dao: FavoritesDAO, user_service: UserService) -> None:
        self.dao = dao
        self.user_service = user_service

    def get_all_favorites(self, token):
        """

        Возвращает список слловарей для избранных фильмов по токуну.

        """
        user_id = self.user_service.get_user_by_token(token).id
        favourite_movies = self.dao.get_all_favorites(user_id)
        favourite_movies_list = []
        for item in favourite_movies:
            favourite_movies_list.append({'id': item.id, 'user_id': item.user, 'movie_id': item.movie})
        return favourite_movies_list

    def update(self, movie_id, token):
        """

        Добавляет избранные фильмы в БД.

        """

        user_id = self.user_service.get_user_by_token(token)
        self.dao.update(user_id.id, movie_id)

    def delete(self, movie_id, token):
        """

        Удаляет фильмы из избранного.

        """

        user_id = self.user_service.get_user_by_token(token)
        self.dao.delete(user_id.id, movie_id)
