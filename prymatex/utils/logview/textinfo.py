# -*- coding: utf-8 -*-
# Copyright © 2011 by Vinay Sajip. All rights reserved. See accompanying LICENSE.txt for details.
from qt import QtCore, QtGui
from ui_textinfo import Ui_TextInfoDialog

class TextInfoDialog(QtGui.QDialog, Ui_TextInfoDialog):
    def __init__(self, parent, info):
        super(TextInfoDialog, self).__init__(parent)
        self.info = info
        self.setupUi(self)

    def setupUi(self, w):
        super(TextInfoDialog, self).setupUi(w)
        self.text.setPlainText(self.info)
        SIGNAL = QtCore.SIGNAL
        self.connect(self.selectAll, SIGNAL('clicked(bool)'), self.on_select_all)
        self.connect(self.copy, SIGNAL('clicked(bool)'), self.on_copy)

    def on_select_all(self, checked=False):
        self.text.selectAll()

    def on_copy(self, checked=False):
        self.text.copy()
