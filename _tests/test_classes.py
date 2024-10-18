"""Integration tests."""

import pytest

from _tests.classes import (
    HTMLTestParser,
    JSONTestParser,
    TxtTestParser,
)
from _tests.expectations import (
    HTML_EXPECTATION,
    JSON_EXPECTATION,
    TXT_EXPECTATION,
)


@pytest.fixture
def html_parser():
    return HTMLTestParser()


@pytest.fixture
def json_parser():
    return JSONTestParser()


@pytest.fixture
def txt_parser():
    return TxtTestParser()


@pytest.fixture
def html_raw():
    with open('raw/1.html', 'r', encoding='utf-8') as f:
        return f.read()


@pytest.fixture
def json_raw():
    with open('raw/1.json', 'r', encoding='utf-8') as f:
        return f.read()


@pytest.fixture
def txt_raw():
    with open('raw/1.txt', 'r', encoding='utf-8') as f:
        return f.read()


def test_html_parser(html_parser, html_raw):
    assert html_parser.parse(html_raw) == HTML_EXPECTATION


def test_json_parser(json_parser, json_raw):
    assert json_parser.parse(json_raw) == JSON_EXPECTATION


def test_txt_parser(txt_parser, txt_raw):
    assert txt_parser.parse(txt_raw) == TXT_EXPECTATION
