from abc import ABC, abstractmethod

from typing_ import ResultT, RawT

__all__ = (
    'ParserI',
)


class ParserI(ABC):

    @abstractmethod
    def bind(self, result: ResultT) -> None:
        pass

    @abstractmethod
    def parse(self, raw: RawT) -> ResultT:
        pass
