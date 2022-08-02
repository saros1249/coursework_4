import calendar
import datetime

import jwt
from flask import current_app

from project.dao.base import BaseDAO
from project.models import User
from project.tools.security import compose_passwords


class UsersDAO(BaseDAO[User]):
    __model__ = User

    def get_by_email(self, email):

        """

        Получение пользователя по EMAIL.

        """

        return self._db_session.query(User).filter(User.email == email).first()

    def create(self, login, password):

        """

        Создание нового пользователя.

        """
        try:
            self._db_session.add(User(email=login, password=password))
            self._db_session.commit()
            return 'Пользователь добавлен'
        except Exception as e:
            self._db_session.rollback()
            return e

    def update(self, user):

        """

         Обновление данных пользователя(имяб фамилияб любимый жанр).

        """
        self._db_session.add(user)
        self._db_session.commit()

    def update_user_password(self, email, new_password):

        """

        Обновление пароля пользователя.

        """

        user = self.get_by_email(email)
        user.password = new_password
        self._db_session.add(user)
        self._db_session.commit()

    def generate_tokens(self, login, password, is_refresh=False):

        """

        Создание токенов.

        """

        user = self.get_by_email(login)

        if not user:
            return False

        if not is_refresh:
            if not compose_passwords(password, user.password):
                return False

        data = {'email': user.email}

        token_expire_min = datetime.datetime.utcnow() + datetime.timedelta(
            minutes=current_app.config['TOKEN_EXPIRE_MINUTES'])
        data['exp'] = calendar.timegm(token_expire_min.timetuple())
        access_token = jwt.encode(data, current_app.config['JWT_SECRET'], algorithm=current_app.config['JWT_ALG'])

        token_expire_day = datetime.datetime.utcnow() + datetime.timedelta(days=current_app.config['TOKEN_EXPIRE_DAYS'])
        data['exp'] = calendar.timegm(token_expire_day.timetuple())
        refresh_token = jwt.encode(data, current_app.config['JWT_SECRET'], algorithm=current_app.config['JWT_ALG'])

        return {'access_token': access_token, 'refresh_token': refresh_token}

    def check_tokens(self, refresh_token):

        """

         Проверка рефреш токенов на идентичность.
         Если True, то создаётся новая пара токенов.

        """
        data = self.data_by_token(refresh_token)
        email = data['email']
        password = data['exp']
        user = self.get_by_email(email)
        if not user:
            return False

        return self.generate_tokens(email, password, is_refresh=True)

    @staticmethod
    def data_by_token(refresh_token):

        """

        Получение данных из токена.

        """
        return jwt.decode(refresh_token, current_app.config['JWT_SECRET'], algorithms=current_app.config['JWT_ALG'])
