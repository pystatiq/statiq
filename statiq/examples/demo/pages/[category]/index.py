from statiq.page import Page

CATEGORIES = {
    "news": {
        "title": "News Category",
        "description": "News page",
        "content": "News content",
    },
    "top": {
        "title": "Top Category",
        "description": "Top page",
        "content": "Top content",
    },
}


def get_path_parameters():
    # Return a list of dicitonaries that will produce the urls and path parameters
    return [
        {
            "category": "news",
        },
        {
            "category": "top",
        },
    ]


def get_page_data(**kwargs):
    category = kwargs.get("category")
    # this method will be called with the path parameters provided in get_path_parameters
    return CATEGORIES[category]


def get_head(**kwargs):
    category = kwargs.get("category")
    return [
        f"<title>{CATEGORIES[category]['title']}</title>",
        "<meta name='viewport' content='width=device-width, initial-scale=1.0'>",
        {
            "tag": "meta",
            "attributes": {
                "name": "description",
                "content": CATEGORIES[category]["description"],
            },
        },
        {
            "tag": "script",
            "attributes": {
                "src": "https://cdn.tailwindcss.com",
            },
        },
    ]


def page():
    return Page(
        data=get_page_data,
        path_parameters=get_path_parameters,
        head=get_head,
    )
