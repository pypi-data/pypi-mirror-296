import functools
from collections.abc import Callable, Iterable, Iterator
from typing import Any, Self, TypeAlias, overload

from markupsafe import Markup, escape

from .attribute import AttributeDict, AttributeValue


class MarkupyElement:
    def __init__(self, name: str) -> None:
        self.name = name
        self.attributes = AttributeDict()
        self.children = None

    def is_void(self) -> bool:
        return self.name in {
            "area",
            "base",
            "br",
            "col",
            "command",
            "embed",
            "hr",
            "img",
            "input",
            "keygen",
            "link",
            "meta",
            "param",
            "source",
            "track",
            "wbr",
        }

    def __iter__(self) -> Iterator[str]:
        if self.name == "html":
            yield "<!doctype html>"

        opening = f"{self.name} {self.attributes}".strip()
        yield f"<{opening}>"
        if not self.is_void():
            yield from iter_node(self.children)
            yield f"</{self.name}>"

    def __str__(self) -> str:
        return Markup("".join(str(x) for x in self))

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} '{self}'>"

    @classmethod
    @functools.lru_cache(maxsize=300)
    def by_name(cls, name: str) -> Self:
        return cls(name)

    def to_element(self) -> "MarkupyElement":
        # When imported, elements are loaded from cache
        # Make sure we re-instantiate them on setting attributes/children
        # to avoid sharing attributes/children between multiple instances
        if self is MarkupyElement.by_name(self.name):
            return MarkupyElement(self.name)
        return self

    # Use call syntax () to define attributes
    @overload
    def __call__(
        self, selector: str, attributes: dict[str, AttributeValue], **kwargs: Any
    ) -> "MarkupyElement": ...
    @overload
    def __call__(self, selector: str, **kwargs: Any) -> "MarkupyElement": ...
    @overload
    def __call__(
        self, attributes: dict[str, AttributeValue], **kwargs: Any
    ) -> "MarkupyElement": ...
    @overload
    def __call__(self, **kwargs: Any) -> Self: ...
    def __call__(self, *args: Any, **kwargs: Any) -> "MarkupyElement":
        selector = None
        attributes_dict = None
        attributes_kwargs = kwargs
        if len(args) == 1:
            if isinstance(args[0], str):
                # element(".foo")
                selector = args[0]
            else:
                # element({"foo": "bar"})
                attributes_dict = args[0]
        elif len(args) == 2:
            # element(".foo", {"bar": "baz"})
            selector, attributes_dict = args

        el = self.to_element()
        try:
            el.attributes.add_selector(selector)
        except ValueError:
            raise ValueError(f"Invalid selector string `{selector}` for element {self}")
        try:
            el.attributes.add_dict(attributes_dict)
        except ValueError:
            raise ValueError(
                f"Invalid dict attributes `{attributes_dict}` for element {self}"
            )
        try:
            el.attributes.add_dict(attributes_kwargs, rewrite_keys=True)
        except ValueError:
            raise ValueError(
                f"Invalid keyword attributes `{attributes_kwargs}` for element {self}"
            )
        return el

    # Use subscriptable [] syntax to assign children
    def __getitem__(self, children: "Node") -> "MarkupyElement":
        if self.is_void():
            raise ValueError(f"Void element {self} cannot contain children")

        el = self.to_element()
        el.children = children
        return el

    # Allow starlette Response.render to directly render this element without
    # explicitly casting to str:
    # https://github.com/encode/starlette/blob/5ed55c441126687106109a3f5e051176f88cd3e6/starlette/responses.py#L44-L49
    def encode(self, encoding: str = "utf-8", errors: str = "strict") -> bytes:
        return str(self).encode(encoding, errors)

    # Avoid having Django "call" a markupy element that is injected into a
    # template. Setting do_not_call_in_templates will prevent Django from doing
    # an extra call:
    # https://docs.djangoproject.com/en/5.0/ref/templates/api/#variables-and-lookups
    do_not_call_in_templates = True


Node: TypeAlias = (
    None | bool | str | int | MarkupyElement | Iterable["Node"] | Callable[[], "Node"]
)


def iter_node(node: Node) -> Iterator[str]:
    if node is None or isinstance(node, bool):
        return
    while not isinstance(node, MarkupyElement) and callable(node):
        node = node()

    if isinstance(node, MarkupyElement):
        yield from node
    elif isinstance(node, int):
        yield str(node)
    elif isinstance(node, str):
        yield str(escape(node))
    elif isinstance(node, Iterable) and not isinstance(node, bytes):
        for child in node:
            yield from iter_node(child)
    else:
        raise ValueError(f"{node!r} is not a valid child element")
