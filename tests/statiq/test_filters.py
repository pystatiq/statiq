from statiq.filters import head_element

def test_head_element_filter_self_closing_tags():
    elements = [
        {
            "element_to_test": {
                "tag": "meta",
                "attributes": {
                    "charset": "utf-8"
                }
            },
            "result": "<meta charset=\"utf-8\" />"
        },
        {
            "element_to_test": {
                "tag": "link",
                "attributes": {
                    "rel": "stylesheet",
                    "href": "css/style.css"
                }
            },
            "result": "<link rel=\"stylesheet\" href=\"css/style.css\" />"
        },
    ]
    for element in elements:
        assert head_element(element["element_to_test"]) == element["result"]

def test_head_element_regular_tags():
    elements = [
        {
            "element_to_test": {
                "tag": "script",
                "attributes": {
                    "src": "js/script.js"
                },
                "content": ""
            },
            "result": "<script src=\"js/script.js\"></script>"
        },
    ]
    for element in elements:
        assert head_element(element["element_to_test"]) == element["result"]

def test_head_element_inline_str():
    elements = [
        "<meta charset=\"utf-8\" />",
        "<link rel=\"stylesheet\" href=\"css/style.css\" />",
        "<script src=\"js/script.js\"></script>",
        "<title>Statiq</title>",
    ]
    for element in elements:
        assert head_element(element) == element
