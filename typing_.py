from typing import TypeVar, Any

__all__ = (
    'RawT',
    'TableT',
    'RecordT',
    'FieldT',
    'FieldValueT',
    'HeaderT',
    'HeadersT',
    'DataRecordT',
    'ResultT',
)

RawT = TypeVar('RawT')
TableT = TypeVar('TableT')
RecordT = TypeVar('RecordT')
FieldT = TypeVar('FieldT')
FieldValueT = TypeVar('FieldValueT')

HeaderT = str
HeadersT = list[HeaderT]

DataRecordT = dict[HeaderT, FieldValueT | Any]
ResultT = dict[str, list[DataRecordT]]
