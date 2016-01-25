#!/usr/bin/env python
# encoding: utf-8

class weixinException(Exception):
    def __init__(self, code, msg):
        self.code = code if code else 0
        self.msg = msg if msg else ''

    @property
    def get_code(self):
        return self.code

    @get_code.setter
    def set_values(self, code):
        self.code = code

class userException(weixinException):
    pass


class dbException(weixinException):
    pass
