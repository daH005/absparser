from abc import ABCMeta
from typing import Callable

from parser_i import ParserI
from designations import Designation

__all__ = (
    'BaseParserMeta',
)


class BaseParserMeta(ABCMeta):

    def __init__(cls, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        if cls.__abstractmethods__:
            return

        cls._special_field_handlers: dict[str, Callable] = {}
        cls._special_fields: list[tuple[str, Callable]] = []
        cls._nested_tables_fields: dict[str, type[ParserI]] = {}

        cls._fill_helpers_by_marks()

    def _fill_helpers_by_marks(cls) -> None:
        for attr_name in dir(cls):
            attr_value = getattr(cls, attr_name)
            mark = getattr(attr_value, Designation.MARK, None)
            if not mark:
                continue

            header = getattr(attr_value, Designation.HEADER)
            if mark == Designation.SPECIAL_FIELD_HANDLER:
                cls._special_field_handlers[header] = attr_value
            elif mark == Designation.SPECIAL_FIELD:
                cls._special_fields.append((header, attr_value))
            elif mark == Designation.NESTED_TABLE_FIELD:
                cls._nested_tables_fields[header] = attr_value
