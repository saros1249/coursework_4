import calendar
import datetime

import jwt

from project.config import JWT_SECRET, JWT_ALG
from project.services.user_service import UserService



class AuthService:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def generate_tokens(self, email, password, is_refresh=False):
        user = self.user_service.get_by_email(email)

        if not user:
            return False

        if not is_refresh:
            if not self.user_service.compare_passwords(password, user.password):
                return False

        data = {'email': user.email}

        min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        data['exp'] = calendar.timegm(min30.timetuple())
        access_token = jwt.encode(data, JWT_SECRET, algorihm=JWT_ALG)

        day130 = datetime.datetime.utcnow() + datetime.timedelta(days=30)
        data['exp'] = calendar.timegm(day130.timetuple())
        refresh_token = jwt.encode(data, JWT_SECRET, algorihm=JWT_ALG)

        return {'access_token': access_token, 'refresh_token': refresh_token}

    def approve_refresh_token(self, refresh_token):
        data = jwt.decode(refresh_token, JWT_SECRET, algorithm=[JWT_ALG])
        email = data['email']
        user = self.user_service.get_by_email(email)

        if not user:
            return False

        now = calendar.timegm(datetime.datetime.utcnow().timetuple())
        expired = data['exp']
        if now > expired:
            return False
        return self.generate_tokens(email, user.password, is_refresh=True)



