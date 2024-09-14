import re
from collections.abc import Iterable
from typing import TypeAlias

from markupsafe import escape

AttributeValue: TypeAlias = None | bool | str | int


def _classes_to_str(classes: Iterable[str]) -> str:
    return " ".join(filter(None, classes))


def _rewrite_attr_key(key: str) -> str:
    # First char "_" not followed by another "_" -> "@"
    key = re.sub(r"^(?:_)([^_]+)", r"@\1", key)
    # Trailing underscore "_" is meaningless and is used to escape protected
    # keywords that might be used as attr keys such as class_ and for_
    key = key.removesuffix("_")
    # Upper case -> "-"
    key = "-".join(filter(None, re.sub(r"([A-Z])", r" \1", key).split())).lower()
    # Double underscore -> ":"
    key = key.replace("__", ":")
    # Single underscore -> "."
    key = key.replace("_", ".")
    return key


class AttributeDict(dict):
    def __setitem__(self, key: str, value: AttributeValue) -> None:
        if not isinstance(key, str):
            raise ValueError("Attribute key must be a string")
        if not isinstance(value, AttributeValue):
            raise ValueError(f"Invalid `{key}` attribute type `{value!r}`")
        if value is False or value is None:
            return

        return super().__setitem__(key, value)

    def __str__(self) -> str:
        pairs = filter(lambda pair: pair[0] and pair[1], self.items())
        return " ".join(
            escape(str(k)) if v is True else f'{escape(str(k))}="{escape(str(v))}"'
            for k, v in pairs
        )

    def add_selector(self, selector: str) -> None:
        if selector is None:
            return
        if not isinstance(selector, str):
            raise ValueError(f"Selector string must be a str, got {selector!r}")

        match = re.match(r"^(#.+?)?(\..+?)?$", selector)
        if match is None:
            raise ValueError("Selector string format is invalid")

        if id_str := match.group(1):
            self["id"] = id_str[1:]
        if cls_str := match.group(2):
            classes = cls_str[1:].split(".")
            self["class"] = _classes_to_str(classes)

    def add_dict(self, dct: dict, *, rewrite_keys: bool = False) -> None:
        if dct is None:
            return
        if not isinstance(dct, dict):
            raise ValueError(f"Attributes must be provided as a dict, got {dct!r}")
        for key, value in dct.items():
            if key != "_" and rewrite_keys:
                # Preserve single _ for hyperscript
                key = _rewrite_attr_key(key)

            if key == "class" and not isinstance(value, str):
                if isinstance(value, dict):
                    # Check for dict before more generic Iterable
                    # Drop all False-ish class values
                    classes = [k for k in value if value[k]]
                    value = _classes_to_str(classes)
                elif isinstance(value, Iterable):
                    value = _classes_to_str(value)

            self[key] = value
