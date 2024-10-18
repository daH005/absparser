__all__ = (
    'HTML_EXPECTATION',
    'JSON_EXPECTATION',
    'TXT_EXPECTATION',
)

HTML_EXPECTATION = {
    'People': [
        {
            'Age': '16',
            'Class': '11',
            'Link': 'https://localhost:8080/danil',
            'Name': 'Данил'
        },
        {
            'Age': '15',
            'Class': '9',
            'Link': 'https://localhost:8081/nastya',
            'Name': 'Настя'
        }
    ]
}

JSON_EXPECTATION = {
    'Numbers': [
        {
            'One': 1,
            'Three': 3,
            'Two': 2},
        {
            'One': 4,
            'Three': 6,
            'Two': 5
        },
        {
            'One': 7,
            'Three': 9,
            'Two': 8
        }
    ]
}

TXT_EXPECTATION = {
    'Articles': [
        {
            'Article': ' 228 ',
            'ID': 1,
            'Part': ' 1 '
        },
        {
            ' Article': ' 337 ',
            'ID': 1,
            'Part': ' 2 '
        }
    ],
    'Clauses': [
        {
            'Clause': ' 5',
            'ID': 2
        },
        {
            'Clause': ' 6',
            'ID': 2
        },
        {
            'Clause': ' а',
            'ID': 2
        },
        {
            'Clause': ' б',
            'ID': 2
        }
    ]
}
