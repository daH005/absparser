from lxml.html import HtmlElement, fromstring
from json import loads as json_loads

from base_parser import BaseParser
from decorators import (
    special_field_handler,
    special_field,
    nested_table_field,
)

__all__ = (
    'HTMLTestParser',
    'JSONTestParser',
    'TxtTestParser',
)


class HTMLTestParser(BaseParser[str, HtmlElement, HtmlElement, HtmlElement, str]):

    _TABLE_NAME = 'People'
    _TRANSLATIONS = {
        'Имя': 'Name',
        'Возраст': 'Age',
        'Класс': 'Class',
        'Ссылка': 'Link',
    }

    def _table_from_raw(self):
        return fromstring(self._raw).xpath('//table')[0]

    def _find_records(self):
        return self._table.xpath('tbody/tr')

    def _find_fields(self):
        return self._record.xpath('td')

    def _find_headers(self):
        return [el.text for el in self._table.xpath('thead/th')]

    def _field_handler(self):
        return self._field.text

    @special_field_handler('Link')
    def _link_field_handler(self) -> str:
        return self._field.xpath('a')[0].get('href')


class JSONTestParser(BaseParser[str, list, list, int, int]):

    _TABLE_NAME = 'Numbers'
    _PREPARED_HEADERS = [
        'One',
        'Two',
        'Three',
    ]

    def _table_from_raw(self):
        return json_loads(self._raw)['structure1']

    def _find_records(self):
        return self._table

    def _find_fields(self):
        return self._record


class TxtTestParser(BaseParser[str, str, str, str, str]):
    _TABLE_NAME = 'Articles'

    def _table_from_raw(self):
        string = self._raw
        string = string.replace(';', '//')
        string = string.replace('ст.', 'Article==')
        string = string.replace('ч.', '/Part==')
        string = string.replace('п.', '/Clauses==')
        return string

    def _find_records(self):
        return self._table.split('//')

    def _find_fields(self):
        return self._record.split('/')

    def _header_field_separator(self):
        return self._field.split('==')

    @special_field('ID')
    def _id_field(self) -> int:
        return 1

    @nested_table_field('Clauses')
    class ClausesParser(BaseParser[str, str, list, str, str]):

        _TABLE_NAME = 'Clauses'
        _PREPARED_HEADERS = ['Clause']

        def _find_records(self):
            return self._table.split(',')

        def _find_fields(self):
            return [self._record]

        @special_field('ID')
        def _id_field(self) -> int:
            return 2
