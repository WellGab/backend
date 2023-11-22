from typing import (
    Any,
    List,
    Sequence,
    Optional,
)
from app.utils.setup import db


class DBMixin:
    """Provides instance of database."""

    def __init__(self) -> None:
        self.db = db


class BaseService(DBMixin):
    """Base class for application services."""


class BaseDataManager(DBMixin):
    """Base data manager class responsible for operations over database."""

    def add_one(self, model: Any) -> Optional[bool]:
        self.session.add(model)

    def add_all(self, models: Sequence[Any]) -> Optional[bool]:
        self.session.add_all(models)

    def get_one(self) -> Optional[Any]:
        return None

    def get_all(self) -> Optional[List[Any]]:
        return None
