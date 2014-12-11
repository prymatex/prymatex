#!/usr/bin/env python
from __future__ import unicode_literals

class StatusMixin(object):
    """docstring for FindMixin"""
    def __init__(self, **kwargs):
        super(StatusMixin, self).__init__(**kwargs)

    def initialize(self, *args, **kwargs):
        super(StatusMixin, self).initialize(*args, **kwargs)
