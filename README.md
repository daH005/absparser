## About the project
I once a lot of worked for code for handling difficult non-structured data from many sites. 
It was data from HTML, JSON, plain text and more. 
In this project I decided to write a library for this task. 

## Usage steps using an example:
0. The raw structure for an example:
```py
raw = 'a=1, b=2, c=3, d=small numbers; a=100, b=200, c=300, d=big numbers'
```

1. Make the imports:
```py
from base_parser import BaseParser
from decorators import special_field_handler
```

2. Inherit `BaseParser` and write the types of: raw, table, record, field and field value:
```py
class MyParser(BaseParser[str, str, str, str, int]): ...
```

3. Write `_TABLE_NAME`:
```py
class MyParser(...):
    _TABLE_NAME = 'MyTable'
    ...
```

4. Implement `_find_records` and `_find_fields`:
```py
class MyParser(...):
    ...
    def _find_records(self):
        return self._table.split('; ')

    def _find_fields(self):
        return self._record.split(', ')
```

5. In this example you have to override `_header_field_separator`:
```py
class MyParser(...):
    ...
    def _header_field_separator(self):
        return self._field.split('=')
```

6. The most field values are numbers (without 'd' field), you have to override `_field_handler`:
```py
class MyParser(...):
    ...
    def _field_handler(self):
        return int(self._field)
```

7. But 'd' field is not a number. You have to use `special_field_handler` decorator:
```py
class MyParser(...):
    ...
    @special_field_handler('d')
    def _d_handler(self):
        return self._field.title()
```

8. We have almost done everything. All that remains is to check `MyParser`:
```py
my_result_to_save = {}

my_parser = MyParser()
my_parser.bind(my_result_to_save)
my_parser.parse(raw)
```

9. After this `my_result_to_save` will contain the following:
```py
{
    'MyTable': [
        {
            'a': 1,
            'b': 2,
            'c': 3,
            'd': 'Small Numbers',
        },
        {
            'a': 100,
            'b': 200,
            'c': 300,
            'd': 'Big Numbers',
        },
    ]
}
```

10. This structure can be easily saved to a SQL-database.

## Rest of the functionality:

```py
base_parser.BaseParser._PREPARED_HEADERS
```
The list of headers in case they are not in `raw`.
A header and a field are matched by index.

---

```py
base_parser.BaseParser._TRANSLATIONS
```
The dictionary for converting bad headers to good headers.

---

```py
base_parser.BaseParser._table_from_raw
```
The method for converting `raw`.

---

```py
base_parser.BaseParser._find_headers
```
The method for search of headers in the table.

---

```py
decorators.special_field
```
The decorator for a field that is not in `_find_fields`.
You have to provide search and handling of a field.

---

```py
decorators.nested_table_field
```
The decorator for a field that contain a nested table.
This decorator works with a parser class.

---

#### I recommend looking at `_tests.classes` to better understand how to build parser classes.
