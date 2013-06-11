#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtCore, QtGui

class DialogManager(QtCore.QObject):
    """
    Object that keep references to non-modal dialog boxes for another QObject,
    typically a QMainWindow or any kind of QWidget
    """
    def __init__(self):
        QtCore.QObject.__init__(self)
        self.dialogs = {}

    def show(self, dialog):
        """Generic method to show a non-modal dialog and keep reference
        to the QtCore.Qt C++ object"""
        for dlg in list(self.dialogs.values()):
            if str(dlg.windowTitle()) == str(dialog.windowTitle()):
                dlg.show()
                dlg.raise_()
                break
        else:
            dialog.show()
            self.dialogs[id(dialog)] = dialog
            self.connect(dialog, QtCore.SIGNAL('accepted()'),
                         lambda eid=id(dialog): self.dialog_finished(eid))
            self.connect(dialog, QtCore.SIGNAL('rejected()'),
                         lambda eid=id(dialog): self.dialog_finished(eid))

    def dialog_finished(self, dialog_id):
        """Manage non-modal dialog boxes"""
        return self.dialogs.pop(dialog_id)

    def close_all(self):
        """Close all opened dialog boxes"""
        for dlg in list(self.dialogs.values()):
            dlg.reject()
