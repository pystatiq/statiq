#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="statiq",
    version="0.0.2",
    author="Marcin Giziński, Krzysztof Koziarek",
    url="http://github.com/pystatiq/statiq",
    author_email="ooizig@gmail.com, krzynio@gmail.com",
    description="Statiq is a static site generator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    entry_points={
        "console_scripts": ["statiq=statiq.cli.commands:main"],
    },
    install_requires=["Jinja2>=3.1.2"],
    package_data={
        "statiq": [
            "examples/demo/config.py",
            "examples/demo/pages/*.py",
            "examples/demo/pages/*/*.py",
            "examples/demo/templates/*.html",
            "examples/demo/templates/*/*.html",
            "templates/*.html",
        ]
    },
)
