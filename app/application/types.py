from abc import ABC, abstractmethod
from typing import TypeVar, Generic
from pydantic import BaseModel

C = TypeVar("C", bound=BaseModel)
Q = TypeVar("Q", bound=BaseModel)


class CommandHandler(ABC, Generic[C]):
    @abstractmethod
    def execute(self, _: C):
        pass


class QueryHandler(ABC, Generic[Q]):
    @abstractmethod
    def execute(self, _: Q):
        pass
