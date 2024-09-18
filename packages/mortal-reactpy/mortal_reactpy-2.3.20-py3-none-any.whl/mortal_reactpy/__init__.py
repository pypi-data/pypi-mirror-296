#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author: MaJian
@Time: 2024/8/22 13:47
@SoftWare: PyCharm
@Project: mortal
@File: __init__.py.py
"""
__all__ = ["MortalReactpy", "html", "comp"]
from .reactpy_main import MortalReactpyMain
from reactpy import html
from reactpy import component as comp


class MortalReactpy(MortalReactpyMain):
    def __init__(self):
        super().__init__()

    def create_app(self, api: list = None):
        return self._create_app(api)

    def configure(self, app, body, head_list: list = None, head_attrs: list = None):
        self._configure(app, body, head_list, head_attrs)

    def run(self, host: str = "127.0.0.1", port: int | None = None, debug: bool = False):
        self._run(host, port, debug)

    def css(self, css_style: str):
        return self._css(css_style)

    def parse(self, contents):
        return self._parse_contents(contents)

    def parse_head_component(self, html_text):
        return self._parse_head(html_text)

    def parse_body_component(self, html_text):
        return self._parse_body(html_text)

    def parse_text(self, html_text):
        return self._parse_text(html_text)
