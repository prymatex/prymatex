#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from PyQt4 import QtGui

from ProgresDialog import ProgressDialog as dialogClass

# {   'title': 'Progress', 
#     'summary': u'Creating HTML version of document\u2026', 
#     'details': '', 
#     'isIndeterminate': True, 
#     'progressAnimate': True
# }

def load(application, settings):
    progress = QtGui.QProgressBar(application.mainWindow)
    progress.show()