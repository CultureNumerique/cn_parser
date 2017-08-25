#!/usr/bin/python3
# -*- coding: utf-8 -*-
from setuptools import setup

try:
    long_description = open("README.rst").read()
except IOError:
    long_description = "Application providing services to parse Esc@pad formated files. Produces HTML websites, EDX or IMS archives."


setup(
    name="cnparser",
    version="0.1",
    url="https://github.com/CultureNumerique/cn_parser",
    description="scripts and parser for IMS, EDX and HTML course generation",
    license="MIT",
    author="Freddy Limpens, Celestine Sauvage UdL, Marc Tommasi - UdL/INRIA",
    author_email="first.last@univ-lille.fr",
    packages=['cnparser'],
    package_dir={'cnparser': 'cnparser'},
    package_data={'cnparser': ['templates/toHTML/*',
                               'templates/toEDX/*',
                               'templates/toEDX/*/*',
                               'templates/toEDX/*/*/*']},
    install_requires=['lxml',
                      'yattag',
                      'markdown',
                      'MarkdownSuperscript',
                      'python-slugify',
                      'pygiftparser',
                      'beautifulsoup4',
                      'jinja2',
                      'requests'],
    long_description=long_description,
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.4",
        "Topic :: Text Processing"
    ],
    entry_points={
        'console_scripts': [
            'cnparser=cnparser.parser:main']}
)
