from project.dao.base import BaseDAO
from project.models import Genre, Movie, Director, User


class GenresDAO(BaseDAO[Genre]):
    __model__ = Genre

class MoviesDAO(BaseDAO[Movie]):
    __model__ = Movie

class DirectorsDAO(BaseDAO[Director]):
    __model__ = Director

class UsersDAO(BaseDAO[User]):
    __model__ = User

