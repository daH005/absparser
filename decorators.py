from typing import Callable, Type

from designations import Designation
from parser_i import ParserI

__all__ = (
    'special_field_handler',
    'special_field',
    'nested_table_field',
)


def special_field_handler(header: str):
    def wrapper(method: Callable):
        setattr(method, Designation.HEADER, header)
        setattr(method, Designation.MARK, Designation.SPECIAL_FIELD_HANDLER)
        return method
    return wrapper


def special_field(header: str):
    def wrapper(method: Callable):
        setattr(method, Designation.HEADER, header)
        setattr(method, Designation.MARK, Designation.SPECIAL_FIELD)
        return method
    return wrapper


def nested_table_field(header: str):
    def wrapper(type_: ParserI):
        setattr(type_, Designation.HEADER, header)
        setattr(type_, Designation.MARK, Designation.NESTED_TABLE_FIELD)
        return type_
    return wrapper
