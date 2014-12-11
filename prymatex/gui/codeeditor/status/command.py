#!/usr/bin/env python
from __future__ import unicode_literals

class CommandMixin(object):
    """docstring for FindMixin"""
    def __init__(self, **kwargs):
        super(CommandMixin, self).__init__(**kwargs)

    def initialize(self, *args, **kwargs):
        super(CommandMixin, self).initialize(*args, **kwargs)
        self.widgetCommand.setVisible(False)
