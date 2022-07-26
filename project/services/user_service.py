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
        return self.dao.get_by_email(email)

    def create(self, login, password):
        password_hash = security.generate_password_hash(password)
        return self.dao.create(login, password_hash)

    def check(self, login, password):
        check_user = self.get_by_email(login)
        user_token = security.generate_tokens(login, password)
        if len(check_user):
            if security.compose_passwords(password, check_user.get('password')):
                security.approve_refresh_token(check_user, user_token.get('refresh_token'))
                return 'Авторизация прошла успешно'
            return 'Неверный пароль'
        return 'Не введён пароль'

    def update(self, email, new_password, old_password):
        new_password = security.generate_password_hash(new_password)
        if self.check(email, old_password):
            self.dao.update(email, new_password)
            return 'Пароль изменён'
        return 'Неверный пароль'


