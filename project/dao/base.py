from typing import Generic, List, Optional, TypeVar

from flask import current_app
from flask_sqlalchemy import BaseQuery
from sqlalchemy import desc
from sqlalchemy.orm import scoped_session
from werkzeug.exceptions import NotFound

from project.container import user_service
from project.models import User
from project.setup.db.models import Base

T = TypeVar('T', bound=Base)


class BaseDAO(Generic[T]):
    __model__ = Base

    def __init__(self, db_session: scoped_session) -> None:
        self._db_session = db_session

    @property
    def _items_per_page(self) -> int:
        return current_app.config['ITEMS_PER_PAGE']

    def get_by_id(self, pk: int) -> Optional[T]:
        return self._db_session.query(self.__model__).get(pk)

    def get_all(self, page: Optional[int] = None) -> List[T]:
        stmt: BaseQuery = self._db_session.query(self.__model__)
        if page:
            try:
                return stmt.paginate(page, self._items_per_page).items
            except NotFound:
                return []
        return stmt.all()

    def get_by_status(self, page: Optional[int] = None, filter=None) -> List[T]:
        stmt = self._db_session.query(self.__model__)
        if filter:
            stmt = stmt.order_by(desc(self.__model__.year))
        if page:
            try:
                return stmt.paginate(page, self._items_per_page).items
            except NotFound:
                return []
        return stmt.all()

    def get_by_email(self, email):
        return self._db_session.query(User).filter(User.email == email).first()

    def create(self, email):
        ent = User(**email)
        self._db_session.add(ent)
        self._db_session.commit()
        return ent

    def update(self, user_d):
        user = self.get_by_id(user_d.get('id'))
        user.name = user_d.get('name')
        user.surname = user_d.get('surname')
        user.favorite_genre = user_d.get('favorite_genre')
        self._db_session.add(user)
        self._db_session.commit()

    def update_user_password(self, email, password, new_password):
        user = self.get_by_email(email.get('password'))
        user_service.compare_passwords(password, new_password)
        user.password = user.get('new_password')
        self._db_session.add(user)
        self._db_session.commit()



