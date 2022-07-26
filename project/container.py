from project.dao import GenresDAO
from project.dao.main import DirectorsDAO, MoviesDAO, UsersDAO

from project.services import GenresService
from project.services.director_service import DirectorsService
from project.services.movie_service import MoviesService
from project.services.user_service import UserService
from project.setup.db import db

# DAO
genre_dao = GenresDAO(db.session)
director_dao = DirectorsDAO(db.session)
movie_dao = MoviesDAO(db.session)
user_dao = UsersDAO(db.session)

# Services
genre_service = GenresService(dao=genre_dao)
director_service = DirectorsService(dao=director_dao)
movie_service = MoviesService(dao=movie_dao)
user_service = UserService(dao=user_dao)

