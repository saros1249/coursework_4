from sqlalchemy import and_

from project.dao.base import BaseDAO
from project.models import Favorites


class FavoritesDAO(BaseDAO[Favorites]):
    __model__ = Favorites



    def update(self, user_id, movie_id):
        try:
            self._db_session.add(Favorites(user_id=user_id, movie_id=movie_id))
            self._db_session.commit()
            return 'Избранный фильм добавлен'
        except Exception as e:
            self._db_session.rollback()
            return e

    def delete(self, user_id, movie_id):
        favorite_id = self._db_session.query(Favorites).filter(and_(Favorites.user_id == user_id, Favorites.movie_id == movie_id)).first()
        self._db_session.delete(favorite_id)
        self._db_session.commit()