#!/usr/bin/env python
from __future__ import unicode_literals

class ReplaceMixin(object):
    """docstring for ReplaceMixin"""
    def __init__(self, **kwargs):
        super(ReplaceMixin, self).__init__(**kwargs)

    def initialize(self, *args, **kwargs):
        self.widgetReplace.setVisible(False)

    # ------- Go to replace
    def replace(self):
        editor = self.window().currentEditor()
        print(editor)

    def showReplace(self):
        self.hideAll()
        self.widgetReplace.setVisible(True)