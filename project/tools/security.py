import base64
import hashlib
import hmac
import calendar
import datetime

import jwt

from flask import current_app

from project.container import user_service
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


def generate_tokens(email, password, is_refresh=False):
    user = user_service.get_by_email(email)

    if not user:
        return False

    if not is_refresh:
        if not compose_passwords(password, user.password):
            return False

    data = {'email': user.email}

    token_expire_min = datetime.datetime.utcnow() + datetime.timedelta(minutes=current_app.config['TOKEN_EXPIRE_MINUTES'])
    data['exp'] = calendar.timegm(token_expire_min.timetuple())
    access_token = jwt.encode(data, secret, algorihm=alg)

    token_expire_day = datetime.datetime.utcnow() + datetime.timedelta(days=current_app.config['TOKEN_EXPIRE_DAYS'])
    data['exp'] = calendar.timegm(token_expire_day.timetuple())
    refresh_token = jwt.encode(data, secret, algorihm=alg)

    return {'access_token': access_token, 'refresh_token': refresh_token}

def approve_refresh_token(refresh_token):
    data = jwt.decode(refresh_token, secret, algorithm=[alg])
    email = data['email']
    user = user_service.get_by_email(email)

    if not user:
        return False

    now = calendar.timegm(datetime.datetime.utcnow().timetuple())
    expired = data['exp']
    if now > expired:
         return False
    return generate_tokens(email, user.password, is_refresh=True)

