from statiq.page import Page


def get_page_data():
    return {
        "title": "Welcome to Statiq",
        "description": "Statiq is a static site generator",
        "content": "Hello world!",
    }


head = [
    # you can use a string to put content in the head
    "<title>Welcome to Statiq</title>",
    "<meta name='viewport' content='width=device-width, initial-scale=1.0'>",
    # or you can use a dictionary to create an element
    {
        "tag": "meta",
        "attributes": {
            "name": "description",
            "content": "Statiq is a static site generator",
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
        head=head,
    )
