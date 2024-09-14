import pytest
from markupsafe import Markup

import markupy
from markupy import MarkupyElement, div


def test_instance_cache() -> None:
    """
    markupy creates element object dynamically. make sure they are reused and case insensitive
    """
    assert markupy.div is markupy.div
    assert markupy.div is markupy.Div
    assert markupy.div is not markupy.div()
    assert markupy.div is not markupy.div[None]


def test_element_repr() -> None:
    assert repr(markupy.div("#a")) == """<MarkupyElement '<div id="a"></div>'>"""


def test_void_element_repr() -> None:
    assert repr(markupy.hr("#a")) == """<MarkupyElement '<hr id="a">'>"""


def test_markup_str() -> None:
    result = str(div(id="a"))
    assert isinstance(result, str)
    assert isinstance(result, Markup)
    assert result == '<div id="a"></div>'


def test_element_type() -> None:
    assert type(div) is MarkupyElement
    assert type(div(a="test")) is MarkupyElement
    assert type(div["a"]) is MarkupyElement
    assert type(div()["a"]) is MarkupyElement
