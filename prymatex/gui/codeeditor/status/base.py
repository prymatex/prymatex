#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtCore, QtGui, QtWidgets
from prymatex.core import PrymatexStatusBar
from prymatex.ui.codeeditor.newstatus import Ui_CodeEditorStatus

from ..editor import CodeEditor

from .find import FindMixin
from .findinfiles import FindInFilesMixin
from .replace import ReplaceMixin

class CodeEditorStatus(PrymatexStatusBar, Ui_CodeEditorStatus, FindMixin,
    FindInFilesMixin, ReplaceMixin,QtWidgets.QWidget):
    def __init__(self, **kwargs):
        super(CodeEditorStatus, self).__init__(**kwargs)
        self.setupUi(self)

    def acceptEditor(self, editor):
        return isinstance(editor, CodeEditor)
        
    def initialize(self, *args, **kwargs):
        print(self.parent(), self.window, args, kwargs)