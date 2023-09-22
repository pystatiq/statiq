from statiq.page import Page

CATEGORIES = {
    "news": {
        "1": {
            "title": "News Category",
            "description": "News page",
            "content": "News content",
        }
    },
    "top": {
        "1": {
            "title": "Top Category",
            "description": "Top page",
            "content": "Top content",
        }
    },
}


def get_path_parameters():
    # Return a list of dicitonaries that will produce the urls and path parameters
    return [
        {"category": "news", "page": "1"},
        {"category": "top", "page": "1"},
    ]


def get_page_data(**kwargs):
    category = kwargs.get("category")
    page = kwargs.get("page")
    # this method will be called with the path parameters provided in get_path_parameters
    return CATEGORIES.get(category).get(page)


def get_head(**kwargs):
    category = kwargs.get("category")
    page = kwargs.get("page")
    return [
        f"<title>{CATEGORIES[category][page]['title']}</title>",
        "<meta name='viewport' content='width=device-width, initial-scale=1.0'>",
        {
            "tag": "meta",
            "attributes": {
                "name": "description",
                "content": CATEGORIES[category][page]["description"],
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
