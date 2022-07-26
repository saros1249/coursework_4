from project.dao import UsersDAO
from project.exceptions import ItemNotFound
from project.models import User
from project.tools import security


class UserService:
    def __init__(self, dao: UsersDAO) -> None:
        self.dao = dao

    def get_one(self, pk: int) -> User:
        if user := self.dao.get_by_id(pk):
            return user
        raise ItemNotFound(f'User with pk={pk} not exists.')

    def get_by_email(self, email):
        return self.dao.get_by_email(email)

    def create(self, login, password):
        password_hash = security.generate_password_hash(password)
        self.dao.create(login, password_hash)
        return 'Новый пользователь создан'

    def update(self, email, user_d):
        self.dao.update(email, user_d)

    def check(self, login, password):
        user_token = self.dao.generate_tokens(login, password)
        if security.compose_passwords(password, self.dao.get_by_email(login).password):
            self.dao.approve_refresh_token(login, user_token.get('refresh_token'))
            return 'Авторизация прошла успешно.'
        return 'Не введён пароль'

    def update_user_password(self, email, old_password, new_password):
        new_password = security.generate_password_hash(new_password)
        if self.check(email, old_password):
            self.dao.update_user_password(email, new_password)
            return 'Пароль изменён'
        return 'Неверный пароль'


