from typing import Union, Dict

SELF_CLOSING_TAGS = [
    "area",
    "base",
    "br",
    "col",
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
]


def head_element(element: Union[str, Dict]) -> str:
    # return rendered head element based on the type of the element
    if isinstance(element, str):
        return element
    elif isinstance(element, dict):
        # start tag
        tag = element["tag"]
        attributes = element["attributes"]
        start_tag = f"<{tag}"
        for attribute, value in attributes.items():
            start_tag += f' {attribute}="{value}"'
        if tag in SELF_CLOSING_TAGS:
            end_tag = " />"
        else:
            start_tag += ">"
            end_tag = f"</{tag}>"
        return start_tag + end_tag
    else:
        raise TypeError(f"Unsupported type: {type(element)}")
