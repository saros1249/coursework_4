import calendar
import datetime

import jwt
from flask import current_app

from project.dao.base import BaseDAO
from project.models import Genre, Movie, Director, User
from project.tools.security import compose_passwords


class GenresDAO(BaseDAO[Genre]):
    __model__ = Genre

class MoviesDAO(BaseDAO[Movie]):
    __model__ = Movie

class DirectorsDAO(BaseDAO[Director]):
    __model__ = Director

class UsersDAO(BaseDAO[User]):
    __model__ = User

    def get_by_email(self, email):
        return self._db_session.query(User).filter(User.email == email).first()

    def create(self, login, password):
        try:
            self._db_session.add(User(email=login, password=password))
            self._db_session.commit()
            return 'Пользователь добавлен'
        except Exception as e:
            self._db_session.rollback()
            return e

    def update(self, email, user_d):
        user = self.get_by_email(email)
        user.name = user_d.get('name')
        user.surname = user_d.get('surname')
        user.favorite_genre = user_d.get('favorite_genre')
        self._db_session.add(user)
        self._db_session.commit()

    def update_user_password(self, email, new_password):
        user = self.get_by_email(email)
        user.password = new_password
        self._db_session.add(user)
        self._db_session.commit()


    def generate_tokens(self, login, password, is_refresh=False):
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


    def approve_refresh_token(self, login, refresh_token):
        data = jwt.decode(refresh_token, current_app.config['JWT_SECRET'], algorithms=current_app.config['JWT_ALG'])
        email = data['email']
        user = self.get_by_email(login)
        if not user:
            return False

        now = calendar.timegm(datetime.datetime.utcnow().timetuple())
        expired = data['exp']
        if now > expired:
            return False
        return self.generate_tokens(email, user.password, is_refresh=True)
