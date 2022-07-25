from project.dao.base import BaseDAO
from project.exceptions import ItemNotFound
from project.models import User
from project.tools import security


class UserService:
    def __init__(self, dao: BaseDAO) -> None:
        self.dao = dao

    def get_one(self, pk: int) -> User:
        if user := self.dao.get_by_id(pk):
            return user
        raise ItemNotFound(f'User with pk={pk} not exists.')

    def get_by_email(self, email):
        return self.dao.create(email)

    def create(self, login, password):
        return self.dao.create(login, password)

    def check(self, login, password):
        check_user = self.get_by_email(login)
        if len(check_user):
            if security.compose_passwords(password, check_user.get('password')):
                return




    def update(self, user_d):
        self.dao.update(user_d)
        return self.dao


