# Statiq: A Python Framework for Static Websites

Statiq is a powerful Python framework designed to simplify the process of generating static websites based on folder structure. Whether you're a developer or a content creator, Statiq provides the tools you need to build beautiful, fast, and secure websites.

## Table of Contents
- [Features](#features)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [Page Object](#page-object)
- [Config](#config)
- [Contributing](#contributing)
## Features

- **Simplicity**: Create static sites based on intuitive folder structures. It will be even easier if you are familiar with frameworks like [Next.js](https://nextjs.org/) or [Gatsby](https://www.gatsbyjs.com/).
- **Customizable**: Leverage `templates` to tailor your site's appearance.
- **Extendable**: Utilize `filters`, and `middleware (coming soon)` to process and modify your content.
- **Command-line Support**: Use the built-in `cli` to manage your projects efficiently.

## Quick Start

1. Install Statiq using `pip`.
   ```sh
    pip install statiq
    ```
2. Initalize the demo project.
   ```sh
   statiq init demo
   ```
3. Build the demo project.
   ```sh
   statiq build
   ```
4. Serve the website.
   ```sh
   python -m http.server --directory build
   ```

## Usage

You need to create two folders to start using Statiq: `pages` and `templates`. The `pages` folder contains all the structure of your website, and the `templates` folder contains all the templates used to render your content.

- **Page** 
  
  A page is a python file that contains a `page()` method.

  The name of the folder will be used as the URL of the page.

  For example, the `about.py` folder will be rendered as `https://example.com/about.html`,
  
  `index.py` will be rendered as `https://example.com/`, and `blog/post.py` will be rendered as `https://example.com/blog/post.html`.

- **Template**
  
  A template is a html file that utilizing Jinja2 syntax. You can use the `{{ content }}` tag to render the content of the page.

## `pages/` folder structure

### Static pages
Simple static pages will be generated based on the structure of the directory and the names of the files. For example, the following structure:
```
pages/index.py
pages/about-us.py
pages/about/index.py
```

will produce the given output:
```
build/index.html
build/about-us.html
build/about/index.html
```
### Dynamic pages
Dynamic pages are pages that are generated based on the `path parameters`.  To define a `path parameter` for a given route you need to put the .py filename or a folder name in `square brackets` 
For example, the following structure:

```
pages/[post].py
pages/[category]/index.py
```

will produce the given output:
```
build/some-post-slug.html
build/other-post-slug.html
build/some-category/index.html
```
### `templates/` folder structure

The templates folder should have the same structure as the `pages/` folder. You can override the template path, for more details see the [Creating a page file](#creating-a-page-file) section.
```
pages/index.py
pages/[post].py
pages/[category]/index.py
```

Should have the corresponding templates:
```
templates/index.html
templates/[post].html
templates/[category]/index.html
```


### Creating a page file

A .py file defining a page should contain a `page()` method. The method should return a `Page` object.

```python
from statiq import Page

def page() -> Page:
    return Page(
        data={
            "title": "Welcome to Statiq",
            "description": "Statiq is a static site generator",
            "content": "Hello world!",
        },
        head=[
            "<title>Welcome to Statiq</title>",
            {
                "tag": "meta",
                "attrs": {"name": "description", "content": "Statiq is a static site generator"},
            }
        ],
    )
```

For more details about using the `Page` object, see the [Page Object](#page-object) section.

## Page Object

The `Page` object is used to define the content of the page. It has the following properties:

- **data**: A `dictionary` or a `Callable` containing the data that will be passed to the template.
- **data**: A `List` or a `Callable` containing the data that will be passed to the template.
- **path_parameters**: A `list` of `dictionaries` or a `Callable` containing the data that will be used to replace the `path parameters` in the route.
- **template_path**: A `string` containing the path to the template that will be used to render the page.

### `data` property

You can define an object or a callable that returns an object. This will be passed to the template

```python

def page() -> Page:
    return Page(
        data={
            "title": "Welcome to Statiq",
            "description": "Statiq is a static site generator",
            "content": "Hello world!",
        },
    )
```

or using a callable

```python
def get_data():
    # do some mojo
    some_data = requests.get("https://example.com/api")
    return some_data.json()

def page() -> Page:
    return Page(
        data=get_data,
    )
```

### `head` property

You can define a list of strings or dictionaries that will be used to generate the `head` section of the page. This can be also a `List` or a `Callable`

**This will only work when your template extends the `base.html` template. Otherwise you need to handle it yourself.**


```python
def my_head()
    return [
        # You can use a string
        "<title>Welcome to Statiq</title>",
        # or a dictionary with the given structure
        {
            "tag": "meta",
            "attributes": {"name": "description", "content": "Statiq is a static site generator"},
        }
    ]

def get_data():
    # do some mojo
    some_data = requests.get("https://example.com/api")
    return some_data.json()

def page() -> Page:
    return Page(
        data=get_data,
        head=my_head,
    )
```

### `path_parameters` property

The `path_parameters` property is used to define the `path parameters` for the given page. It should be a list of dictionaries. 
The object should be a `List` containing `dictionaries` with all the `path parameters` that will be used to generate the page.

```python
# /pages/[post].py

def page() -> Page:
    return Page(
        data={
            "title": "Welcome to Statiq",
            "description": "Statiq is a static site generator",
            "content": "Hello world!",
        },
        path_parameters=[
            {"post": "some-post-slug"},
            {"post": "other-post-slug"},
        ],
    )
```

### Passing `path parameters` to `data` and `head` properties

For routes that utilize `path parameters` they will be expanded and passed as a keyword argument to the `data` and `head` properties.

```python
# /pages/[post].py

def get_path_parameters():
    return [
        {"post": "some-post-slug"},
        {"post": "other-post-slug"},
    ]

def get_data(**kwargs):
    post = kwargs.get("post")
    # do some mojo
    some_data = requests.get(f"https://example.com/api/{post}")
    return some_data.json()

def get_head(**kwargs):
    post = kwargs.get("post")
    return [
        # You can use a string
        f"<title>{post}</title>",
        # or a dictionary with the given structure
        {
            "tag": "meta",
            "attributes": {"name": "description", "content": post},
        }
    ]

def page() -> Page:
    return Page(
        data=get_data,
        head=get_head,
        path_parameters=get_path_parameters,
    )
```

### Example with multiple `path parameters`

```python
# /pages/[category]/[post].py

def get_path_parameters():
    return [
        {"category": "some-category", "post": "some-post-slug"},
        {"category": "other-category", "post": "other-post-slug"},
    ]

def get_data(**kwargs):
    category = kwargs.get("category")
    post = kwargs.get("post")
    # do some mojo
    some_data = requests.get(f"https://example.com/api/{category}/{post}")
    return some_data.json()

def get_head(**kwargs):
    category = kwargs.get("category")
    post = kwargs.get("post")
    return [
        # You can use a string
        f"<title>{category} - {post}</title>",
        # or a dictionary with the given structure
        {
            "tag": "meta",
            "attributes": {"name": "description", "content": post},
        }
    ]

def page() -> Page:
    return Page(
        data=get_data,
        head=get_head,
        path_parameters=get_path_parameters,
    )
```

### `template_path` property

The `template_path` property is used to define the path to the template that will be used to render the page. If the property is not defined the page will be rendered using the `index.html` template.

```python
def page() -> Page:
    return Page(
        data={
            "title": "Welcome to Statiq",
            "description": "Statiq is a static site generator",
            "content": "Hello world!",
        },
        template_path="custom.html",
    )
```

## Config
To add a custom configuration to your project you need to create a `config.py` file in the root of your project. 

### Custom filters
To add your own custom template [filters](https://jinja.palletsprojects.com/en/3.1.x/templates/#filters) you need to define a `FILTERS` dictionary in your `config.py` file. The key of the dictionary will be the name of the filter and the value should be a callable.


```python
# config.py
from my_filters import my_filter, my_other_filter

FILTERS = {
    "my_filter": my_filter,
    "my_other_filter": my_other_filter,
}
```

### Globals 
To add [global variables](https://jinja.palletsprojects.com/en/3.1.x/api/#global-namespace) to your templates you need to define a `GLOBALS` dictionary in your `config.py` file. The key of the dictionary will be the name of the variable and the value can be an object or a callable.

```python
# config.py

GLOBALS = {
    "my_global": "some value",
    "my_other_global": lambda: "some other value",
}
```
