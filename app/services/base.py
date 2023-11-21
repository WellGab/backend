from typing import (
    Any,
    List,
    Sequence,
    Optional,
)

class BaseService():
    """Base class for application services."""


class BaseDataManager():
    """Base data manager class responsible for operations over database."""

    def add_one(self, model: Any) -> Optional[bool]:
        self.session.add(model)

    def add_all(self, models: Sequence[Any]) -> Optional[bool]:
        self.session.add_all(models)

    def get_one(self) -> Optional[Any]:
        return None

    def get_all(self) -> Optional[List[Any]]:
        return None