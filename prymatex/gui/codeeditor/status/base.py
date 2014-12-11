#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtCore, QtGui, QtWidgets
from prymatex.core import PrymatexStatusBar
from prymatex.ui.codeeditor.newstatus import Ui_CodeEditorStatus

from ..editor import CodeEditor

from .find import FindMixin
from .findinfiles import FindInFilesMixin
from .replace import ReplaceMixin
from .command import CommandMixin
from .status import StatusMixin

class CodeEditorStatus(PrymatexStatusBar, FindMixin, FindInFilesMixin,
    ReplaceMixin, CommandMixin, StatusMixin, Ui_CodeEditorStatus, QtWidgets.QWidget):
    def __init__(self, **kwargs):
        super(CodeEditorStatus, self).__init__(**kwargs)
        self.setupUi(self)

    def acceptEditor(self, editor):
        return isinstance(editor, CodeEditor)
        
    def initialize(self, *args, **kwargs):
        super(CodeEditorStatus, self).initialize(*args, **kwargs)
        #print(self.parent(), self.window, args, kwargs)
