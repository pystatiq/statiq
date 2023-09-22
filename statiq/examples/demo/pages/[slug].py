from statiq.page import Page

ARTICLES = {
    "about": {
        "title": "About",
        "description": "About page",
        "content": "About content",
    },
    "contact": {
        "title": "Contact",
        "description": "Contact page",
        "content": "Contact content",
    },
}


def get_path_parameters():
    # Return a list of dicitonaries that will produce the urls and path parameters
    return [
        {
            "slug": "about",
        },
        {
            "slug": "contact",
        },
    ]


def get_page_data(slug):
    # this method will be called with the path parameters provided in get_path_parameters
    return ARTICLES[slug]


def get_head(slug):
    return [
        f"<title>{ARTICLES[slug]['title']}</title>",
        "<meta name='viewport' content='width=device-width, initial-scale=1.0'>",
        {
            "tag": "meta",
            "attributes": {
                "name": "description",
                "content": ARTICLES[slug]["description"],
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
