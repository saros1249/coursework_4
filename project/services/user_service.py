from flask import request

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
            return self.dao.generate_tokens(login, user_token.get('refresh_token'))



    def update_user_password(self, user_d):
        new_password = security.generate_password_hash(user_d.get('new_password'))
        if self.check(user_d.get('email'), user_d.get('password')):
            return self.dao.update_user_password(user_d.get('email'), new_password)



    def check_tokens(self, refresh_token):
      return self.dao.check_tokens(refresh_token)


    def get_user_by_token(self, refresh_token):
        data = self.dao.data_by_token(refresh_token)

        if data:
            return self.get_by_email(data.get('email'))




