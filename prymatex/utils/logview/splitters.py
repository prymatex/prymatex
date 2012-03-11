# -*- coding: utf-8 -*-
# Copyright © 2011 by Vinay Sajip. All rights reserved. See accompanying LICENSE.txt for details.
from qt import QtCore, QtGui

class SplitterHandle(QtGui.QSplitterHandle):
    def mouseDoubleClickEvent(self, event):
        super(SplitterHandle, self).mouseDoubleClickEvent(event)
        splitter = self.splitter()
        index = splitter.indexOf(self)
        splitter.emit(QtCore.SIGNAL('doubleClicked(int,int)'), index, int(event.buttons()))

class Splitter(QtGui.QSplitter):
    def createHandle(self):
        return SplitterHandle(self.orientation(), self)
