from typing import Generic, Iterable
from abc import abstractmethod

from base_parser_meta import BaseParserMeta
from typing_ import (
    RawT,
    TableT,
    RecordT,
    FieldT,
    FieldValueT,
    HeaderT,
    HeadersT,
    ResultT,
    DataRecordT,
)
from parser_i import ParserI

__all__ = (
    'BaseParser',
)


class BaseParser(ParserI, Generic[RawT, TableT, RecordT, FieldT, FieldValueT], metaclass=BaseParserMeta):
    """The base class of parsers.
    The idea is that `parser.parse(raw)` converts `raw` into a list of dictionaries,
    that is, records for a SQL-database and stores this list in the result by `_TABLE_NAME` key.

    Usage steps using an example:\n
    0. The raw structure for an example::
        raw = 'a=1, b=2, c=3, d=small numbers; a=100, b=200, c=300, d=big numbers'

    1. Make the imports::
        from base_parser import BaseParser\n
        from decorators import special_field_handler

    2. Inherit this class and write the types of: raw, table, record, field and field value::
        class MyParser(BaseParser[str, str, str, str, int]): ...

    3. Write `_TABLE_NAME`::
        class MyParser(...):
            _TABLE_NAME = 'MyTable'\n
            ...

    4. Implement `_find_records` and `_find_fields`::
        class MyParser(...):
            ...\n
            def _find_records(self):
                return self._table.split('; ')

            def _find_fields(self):
                return self._record.split(', ')

    5. In this example you have to override `_header_field_separator`::
        class MyParser(...):
            ...\n
            def _header_field_separator(self):
                return self._field.split('=')

    6. The most field values are numbers (without 'd' field), you have to override `_field_handler`::
        class MyParser(...):
            ...\n
            def _field_handler(self):
                return int(self._field)

    7. But 'd' field is not a number. You have to use `special_field_handler` decorator::
        class MyParser(...):
            ...\n
            @special_field_handler('d')\n
            def _d_handler(self):
                return self._field.title()

    8. We have almost done everything. All that remains is to check `MyParser`::
        my_result_to_save = {}

        my_parser = MyParser()\n
        my_parser.bind(my_result_to_save)\n
        my_parser.parse(raw)

    9. After this `my_result_to_save` will contain the following::
        {
            'MyTable': [
                {
                    'a': 1,\n
                    'b': 2,\n
                    'c': 3,\n
                    'd': 'Small Numbers',\n
                },\n
                {
                    'a': 100,\n
                    'b': 200,\n
                    'c': 300,\n
                    'd': 'Big Numbers',
                },
            ]
        }

    10. This structure can be easily saved to a SQL-database.
    """

    # Annotations:
    _result: ResultT
    _data_record: DataRecordT

    _raw: RawT
    _table: TableT

    _records: Iterable[RecordT]
    _record_i: int
    _record: RecordT

    _fields: Iterable[FieldT]
    _field_i: int
    _field: FieldT
    _field_value: FieldValueT

    _headers: HeadersT
    _header: HeaderT
    # End of annotations.

    _TABLE_NAME: str
    """Must be implemented."""
    _PREPARED_HEADERS: list[HeaderT] = []
    """Can be overridden."""
    _TRANSLATIONS: dict[HeaderT, HeadersT] = {}
    """Can be overridden."""

    def __init__(self) -> None:
        self.bind({})

    def bind(self, result: dict) -> None:
        self._result = result

    def parse(self, raw: RawT) -> ResultT:
        self._raw = raw

        self._result.setdefault(self._TABLE_NAME, [])
        self._table = self._table_from_raw()
        self._make_headers()
        self._iter_records()

        if not self._result[self._TABLE_NAME]:
            self._result.pop(self._TABLE_NAME)

        return self._result

    def _table_from_raw(self) -> TableT:
        """Can be overridden."""
        return self._raw

    def _make_headers(self) -> None:
        self._headers = []
        for header in self._find_headers():
            header = self._TRANSLATIONS.get(header, header)
            self._headers.append(header)

    def _find_headers(self) -> Iterable[HeaderT]:
        """Can be overridden."""
        yield from self._PREPARED_HEADERS

    def _iter_records(self) -> None:
        self._records = self._find_records()
        for self._record_i, self._record in enumerate(self._records):
            self._data_record = {}
            self._iter_fields()
            self._iter_special_fields()
            self._add_data_record_if_it_exist()

    @abstractmethod
    def _find_records(self) -> Iterable[RecordT]:
        """Must be implemented."""
        pass

    def _iter_fields(self) -> None:
        self._fields = self._find_fields()
        for self._field_i, self._field in enumerate(self._fields):
            self._header, self._field = self._header_and_field()
            self._handle_field_and_save_data()

    @abstractmethod
    def _find_fields(self) -> Iterable[FieldT]:
        """Must be implemented."""
        pass

    def _header_and_field(self) -> tuple[HeaderT, FieldT]:
        try:
            return self._headers[self._field_i], self._field
        except IndexError:
            return self._header_field_separator()

    def _header_field_separator(self) -> tuple[HeaderT, FieldT]:
        """Can be overridden."""
        raise NotImplemented

    def _handle_field_and_save_data(self) -> None:
        if self._header in self._special_field_handlers:
            self._data_record[self._header] = self._special_field_handlers[self._header](self)

        elif self._header in self._nested_tables_fields:
            sub_parser = self._nested_tables_fields[self._header]()
            sub_parser.bind(self._result)
            sub_parser.parse(self._field)

        else:
            self._data_record[self._header] = self._field_handler()

    def _field_handler(self) -> FieldValueT:
        """Can be overridden."""
        return self._field

    def _iter_special_fields(self) -> None:
        for header, handler in self._special_fields:
            self._data_record[header] = handler(self)

    def _add_data_record_if_it_exist(self) -> None:
        self._result[self._TABLE_NAME].append(self._data_record)
