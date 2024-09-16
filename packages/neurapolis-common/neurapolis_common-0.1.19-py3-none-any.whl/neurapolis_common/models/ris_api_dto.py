from abc import ABC, abstractmethod
from typing import TypeVar

T = TypeVar("T", bound="RisApiDto")


class RisApiDto(ABC):
    @classmethod
    @abstractmethod
    def from_ris_api_dto(cls, ris_api_dto: dict) -> T:
        pass
