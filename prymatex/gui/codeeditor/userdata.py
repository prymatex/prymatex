#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import namedtuple

from prymatex.qt import QtGui
from prymatex.support import Scope

class CodeEditorToken(namedtuple('CodeEditorToken', 'start end scope chunk')):
    __slots__ = ()
    @property
    def group(self):
        return self.scope.rootGroupName()

_empty_token = CodeEditorToken(0, 0, Scope(), "")

class CodeEditorBlockUserData_Meta(type(QtGui.QTextBlockUserData), type(namedtuple)):
     pass   

class CodeEditorBlockUserData(QtGui.QTextBlockUserData, namedtuple('CodeEditorBlockUserData', 'tokens state revision indentation blank')):
    __metaclass__ = CodeEditorBlockUserData_Meta
    def tokenAt(self, pos):
        for token in self.tokens[::-1]:
            if token.start <= pos < token.end:
                return token
        return _empty_token

_empty_user_data = CodeEditorBlockUserData((), -1, -1, "", True)
