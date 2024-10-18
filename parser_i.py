from abc import ABC

from typing_ import ResultT, RawT

__all__ = (
    'ParserI',
)


class ParserI(ABC):

    def bind(self, result: ResultT) -> None:
        pass

    def parse(self, raw: RawT) -> ResultT:
        pass
