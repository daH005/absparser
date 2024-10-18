from enum import StrEnum

__all__ = (
    'Designation',
)


class Designation(StrEnum):
    HEADER = 'header'
    MARK = 'mark'

    SPECIAL_FIELD_HANDLER = 'special_field_handler'
    SPECIAL_FIELD = 'special_field'
    NESTED_TABLE_FIELD = 'nested_table_field'
