import jwt
from flask import request, abort, current_app


def auth_required(func):
    """
    Проверка аутетификации пользователя.
    """

    def wrapper(*args, **kwargs):
        if not 'Authorization' in request.headers:
            abort(401)

        token = request.headers['Authorization']
        try:
            jwt.decode(token, current_app.config['JWT_SECRET'], algorithms=current_app.config['JWT_ALG'])
        except Exception as e:
            print(f'JWT decode error: {e}')
            abort(401)
        return func(*args, **kwargs)

    return wrapper
