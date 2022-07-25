import base64
import hashlib
import hmac
import calendar
import datetime

import jwt

from flask import current_app
from project.services.user_service import UserService

secret = current_app.config['JWT_SECRET']
alg = current_app.config['JWT_ALG']

def __generate_password_digest(password: str) -> bytes:
    return hashlib.pbkdf2_hmac(
        hash_name="sha256",
        password=password.encode("utf-8"),
        salt=current_app.config["PWD_HASH_SALT"],
        iterations=current_app.config["PWD_HASH_ITERATIONS"],
    )


def generate_password_hash(password: str) -> str:
    return base64.b64encode(__generate_password_digest(password)).decode('utf-8')


def compose_passwords(password, password_hash):
    return generate_password_hash(password) == password_hash





class AuthService:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def generate_tokens(self, email, password, is_refresh=False):
        user = self.user_service.get_by_email(email)

        if not user:
            return False

        if not is_refresh:
            if not compose_passwords(password, user.password):
                return False

        data = {'email': user.email}

        min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        data['exp'] = calendar.timegm(min30.timetuple())
        access_token = jwt.encode(data, secret, algorihm=alg)

        day130 = datetime.datetime.utcnow() + datetime.timedelta(days=30)
        data['exp'] = calendar.timegm(day130.timetuple())
        refresh_token = jwt.encode(data, secret, algorihm=alg)

        return {'access_token': access_token, 'refresh_token': refresh_token}

    def approve_refresh_token(self, refresh_token):
        data = jwt.decode(refresh_token, secret, algorithm=[alg])
        email = data['email']
        user = self.user_service.get_by_email(email)

        if not user:
            return False

        now = calendar.timegm(datetime.datetime.utcnow().timetuple())
        expired = data['exp']
        if now > expired:
            return False
        return self.generate_tokens(email, user.password, is_refresh=True)

