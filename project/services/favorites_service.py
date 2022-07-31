from project.dao.favorites_dao import FavoritesDAO
from project.exceptions import ItemNotFound


class FavoritesService:
    def __init__(self, dao: FavoritesDAO) -> None:
        self.dao = dao

    # def get_one(self, pk: int) -> User:
    #     if user := self.dao.get_by_id(pk):
    #         return user
    #     raise ItemNotFound(f'User with pk={pk} not exists.')
    #
    #
    # def create(self, login, password):
    #     password_hash = security.generate_password_hash(password)
    #     self.dao.generate_tokens(login, password_hash)
    #     self.dao.create(login, password_hash)
    #     return 'Новый пользователь создан'
    #
    # def update(self, email, user_d):
    #     self.dao.update(email, user_d)
    #

