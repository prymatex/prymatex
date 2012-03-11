# -*- coding: utf-8 -*-
# Copyright © 2011 by Vinay Sajip. All rights reserved. See accompanying LICENSE.txt for details.

from qt import QtCore, QtGui, QT_VERSION_STR, PYQT_VERSION_STR, WRAPPER

from ui_about import Ui_AboutDialog

class AboutDialog(QtGui.QDialog, Ui_AboutDialog):
    def __init__(self, parent):
        super(AboutDialog, self).__init__(parent)
        self.setupUi(self)
        args = (WRAPPER, PYQT_VERSION_STR, QT_VERSION_STR)
        self.qtversion.setText('%s version %s on Qt version %s' % args)
