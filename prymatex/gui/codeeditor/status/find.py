#!/usr/bin/env python
from __future__ import unicode_literals

class FindMixin(object):
    """docstring for FindMixin"""
    def __init__(self, **kwargs):
        super(FindMixin, self).__init__(**kwargs)

    def initialize(self, *args, **kwargs):
        self.widgetFind.setVisible(False)

    def showFind(self):
        self.hideAll()
        self.widgetFind.setVisible(True)