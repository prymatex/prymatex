#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import namedtuple

from prymatex.qt import QtGui
from prymatex.support import Scope

from prymatex.support import PreferenceMasterSettings

class CodeEditorToken(namedtuple('CodeEditorToken', 'start end scope chunk')):
    __slots__ = ()
    @property
    def group(self):
        return self.scope.rootGroupName()

class CodeEditorBlockUserData(QtGui.QTextBlockUserData):
    __slots__ = ('tokens', 'state', 'revision', 'indentation', 'blank')
    def __init__(self, tokens, state, revision, indentation, blank):
        super(CodeEditorBlockUserData, self).__init__()
        self.tokens = tokens
        self.state = state
        self.revision = revision
        self.indentation = indentation
        self.blank = blank

    @property
    def foldingMark(self):
        return PreferenceMasterSettings.FOLDING_NONE

    def tokenAt(self, pos):
        # TODO Validar que pos "<= token.end" funcione bien porque puede ser tenga 
        # que obtener la mejor opcion buscando entre dos candidatos
        for token in self.tokens[::-1]:
            if token.start <= pos <= token.end:
                return token
