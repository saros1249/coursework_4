from project.dao.user_dao import UsersDAO
from project.exceptions import ItemNotFound
from project.models import User
from project.tools import security


class UserService:
    def __init__(self, dao: UsersDAO) -> None:
        self.dao = dao

    def get_one(self, pk: int) -> User:

        """

        Получение пользователя по ID.

        """
        if user := self.dao.get_by_id(pk):
            return user
        raise ItemNotFound(f'User with pk={pk} not exists.')

    def get_by_email(self, email):

        """

        Получение пользователя по EMAIL.

        """
        return self.dao.get_by_email(email)

    def create(self, login, password):

        """

        Создание нового пользователя.

        """
        password_hash = security.generate_password_hash(password)
        self.dao.generate_tokens(login, password_hash)
        self.dao.create(login, password_hash)
        return 'Новый пользователь создан'

    def update(self, token, user_d):

        """

        Обновление данных пользователя(имя, фамилия, любимый жанр).

        """

        user = self.get_by_email(self.dao.data_by_token(token).get('email'))
        if 'name' in user_d:
            user.name = user_d.get('name')
        if 'surname' in user_d:
            user.surname = user_d.get('surname')
        if 'favorite_genre' in user_d:
            user.favorite_genre = user_d.get('favorite_genre')
        return self.dao.update(user)

    def check(self, login, password):

        """

        Создание токена(там же проверка логина и пароля).

        """

        return self.dao.generate_tokens(login, password)

    def check_tokens(self, token):

        """

         Проверка рефреш токенов на идентичность.
         Если True, то создаётся новая пара токенов.

        """

        return self.dao.check_tokens(token)

    def update_user_password(self, token, user_d):

        """

        Изменение пароля входа.

        """

        new_password = security.generate_password_hash(user_d.get('new_password'))
        if self.check(user_d.get('email'), user_d.get('old_password')):
            return self.dao.update_user_password(self.get_user_by_token(token), new_password)

    def get_user_by_token(self, refresh_token):

        """

        Получение данных авторизованного пользователя по токену.

        """
        data = self.dao.data_by_token(refresh_token)
        if data:
            return self.get_by_email(data.get('email'))
