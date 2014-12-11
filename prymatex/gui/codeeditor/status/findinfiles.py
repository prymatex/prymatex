#!/usr/bin/env python
from __future__ import unicode_literals

class FindInFilesMixin(object):
    """docstring for FindInFilesMixin"""
    def __init__(self, **kwargs):
        super(FindInFilesMixin, self).__init__(**kwargs)

    def initialize(self, *args, **kwargs):
        super(FindInFilesMixin, self).initialize(*args, **kwargs)
        self.widgetFindInFiles.setVisible(False)
