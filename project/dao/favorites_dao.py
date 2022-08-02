from sqlalchemy import and_

from project.dao.base import BaseDAO
from project.models import Favorites


class FavoritesDAO(BaseDAO[Favorites]):
    __model__ = Favorites

    def get_all_favorites(self, user_id):
        """

        Получает из базы избранные фильмы по ID пользователя.

        """

        favorite_data = self._db_session.query(Favorites).filter(Favorites.user_id == user_id).all()
        return favorite_data

    def update(self, user_id, movie_id):
        """

         Добавляет в БД избранный фильм.

        """

        try:
            self._db_session.add(Favorites(user_id=user_id, movie_id=movie_id))
            self._db_session.commit()
            return 'Избранный фильм добавлен'
        except Exception as e:
            self._db_session.rollback()
            return e

    def delete(self, user_id, movie_id):

        """

        Удаляет из БД избранный фильм.

        """
        favorite_id = self._db_session.query(Favorites).filter(
            and_(Favorites.user_id == user_id, Favorites.movie_id == movie_id)).first()
        self._db_session.delete(favorite_id)
        self._db_session.commit()
        return 'Избранный фильм удалён.'
