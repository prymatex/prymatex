#!/usr/bin/env python
#-*- encoding: utf-8 -*-
# Created: 04/02/2010 by defo

from gui.mywidget import MyWidget

from PyQt4.Qt import *
import sys
app = QApplication(sys.argv)
win = MyWidget()

win.show()
sys.exit(app.exec_())