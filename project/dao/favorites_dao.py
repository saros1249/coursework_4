from project.dao.base import BaseDAO
from project.models import Favorites_genres


class FavoritesDAO(BaseDAO[Favorites_genres]):
    __model__ = Favorites_genres

    def get(self):
        pass

    def create(self, user_id, genre_id):
        try:
            self._db_session.add(Favorites_genres(user_id=user_id, genre_id=genre_id))
            self._db_session.commit()
            return 'Избранный жанр добавлен'
        except Exception as e:
            self._db_session.rollback()
            return e

    def delete(self, user_id, genre_id):
        pass