import base64
import hashlib
import hmac
from typing import Optional

from project.config import PWD_HASH_SALT, PWD_HASH_ITERATIONS
from project.dao.base import BaseDAO
from project.exceptions import ItemNotFound
from project.models import User


class UserService:
    def __init__(self, dao: BaseDAO) -> None:
        self.dao = dao

    def get_one(self, pk: int) -> User:
        if user := self.dao.get_by_id(pk):
            return user
        raise ItemNotFound(f'User with pk={pk} not exists.')

    def get_by_email(self, email):
        return self.dao.get_by_email(email)

    def create(self, user_d):
        return self.dao.create(user_d)

    def update(self, user_d):
        self.dao.update(user_d)
        return self.dao

    def get_password_hash(self, password):
        return base64.b64encode(hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        ))

    def compare_passwords(self, password, password_hash):
        return hmac.compare_digest(base64.b64decode(password_hash), base64.b64decode(self.get_password_hash(password)))