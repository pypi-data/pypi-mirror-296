#!/usr/bin/env python

"""setup.py: distutils/setuptools install script."""

from setuptools import setup, find_packages

REQUIRES = [
    "Django>=4,<6",
]

try:
    with open("README.md", encoding="utf-8") as f:
        LONG_DESCRIPTION = f.read()
except FileNotFoundError:
    LONG_DESCRIPTION = ""

setup(
    name="django-permalinker",
    version="0.1.1",
    author="Efficient Solutions LLC",
    author_email="contact@efficient.solutions",
    description="Django application to create, manage, and redirect permanent links",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/efficient-solutions/django-permalinker",
    packages=find_packages(include=["django_permalinker", "django_permalinker.*"]),
    license="MIT",
    install_requires=REQUIRES,
    python_requires=">= 3.10",
    include_package_data=True,
    keywords=[
        "Django", "Permanent links", "Permalinks", "URL Shortener"
    ],
    classifiers=[
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ]
)
