import re as _re

from markupsafe import Markup as _Markup

from .element import MarkupyElement, Node, iter_node


def render_node(node: Node) -> _Markup:
    return _Markup("".join(iter_node(node)))


def __getattr__(name: str) -> MarkupyElement:
    # Consider uppercase chars and underscores as word boundaries for tag names
    words = filter(None, _re.sub(r"([A-Z])", r"_\1", name).split("_"))
    html_name = "-".join(words).lower()
    return MarkupyElement.by_name(html_name)
