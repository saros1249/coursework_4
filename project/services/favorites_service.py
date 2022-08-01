
from project.dao.favorites_dao import FavoritesDAO
from project.services import UserService


class FavoritesService:
    def __init__(self, dao: FavoritesDAO, user_service: UserService) -> None:
        self.dao = dao
        self.user_service = user_service

    def get_all(self):
        return self.dao.get_all()

    def update(self, movie_id, token):
        user_id = self.user_service.get_user_by_token(token)
        self.dao.update(user_id.id, movie_id)


    def delete(self, movie_id, token):
        user_id = self.user_service.get_user_by_token(token)
        self.dao.delete(user_id.id, movie_id)
