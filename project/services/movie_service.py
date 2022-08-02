from typing import Optional

from project.dao.base import BaseDAO
from project.exceptions import ItemNotFound
from project.models import Movie


class MoviesService:
    def __init__(self, dao: BaseDAO) -> None:
        self.dao = dao

    def get_item(self, pk: int) -> Movie:
        """

        Получение фильма по ID.

        """
        if movie := self.dao.get_by_id(pk):
            return movie
        raise ItemNotFound(f'[Movie with pk={pk} not exists.')

    def get_all(self, filter=None, page: Optional[int] = None) -> list[Movie]:
        """

        Получение списка всех жанров.

        """
        return self.dao.get_by_status(filter_status=filter, page=page)
