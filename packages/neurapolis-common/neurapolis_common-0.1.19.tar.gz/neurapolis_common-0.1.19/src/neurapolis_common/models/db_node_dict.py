from abc import ABC, abstractmethod
from typing import TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound="DbNodeDict")


class DbNodeDict(ABC):
    @classmethod
    @abstractmethod
    def from_db_node_dict(cls, db_node_dict: dict) -> T:
        pass

    @abstractmethod
    def to_db_node_dict(self) -> dict:
        pass
