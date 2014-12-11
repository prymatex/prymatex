#!/usr/bin/env python
from __future__ import unicode_literals

class ReplaceMixin(object):
    """docstring for ReplaceMixin"""
    def __init__(self, **kwargs):
        super(ReplaceMixin, self).__init__(**kwargs)

    def initialize(self, *args, **kwargs):
        super(ReplaceMixin, self).initialize(*args, **kwargs)
        print("Replace")
        self.widgetReplace.setVisible(False)
