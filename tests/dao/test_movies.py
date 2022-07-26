import pytest

from project.dao import MoviesDAO
from project.models import Movie


class TestMoviessDAO:

    @pytest.fixture
    def movies_dao(self, db):
        return MoviesDAO(db.session)

    @pytest.fixture
    def movie_1(self, db):
        m = Movie(name="Allen")
        db.session.add(g)
        db.session.commit()
        return m

    @pytest.fixture
    def movie_2(self, db):
        m = Movie(name="Sheppard")
        db.session.add(m)
        db.session.commit()
        return m

    def test_get_movie_by_id(self, movie_1, movies_dao):
        assert movies_dao.get_by_id(movie_1.id) == movie_1

    def test_get_movie_by_id_not_found(self, movies_dao):
        assert not movies_dao.get_by_id(1)

    def test_get_all_movies(self, movies_dao, movie_1, movie_2):
        assert movies_dao.get_all() == [movie_1, movie_2]

    def test_get_movies_by_page(self, app, movies_dao, movie_1, movie_2):
        app.config['ITEMS_PER_PAGE'] = 1
        assert movies_dao.get_all(page=1) == [movier_1]
        assert movies_dao.get_all(page=2) == [movier_2]
        assert movies_dao.get_all(page=3) == []
