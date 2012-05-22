# -*- coding: utf-8 -*-
# Copyright © 2011 by Vinay Sajip. All rights reserved. See accompanying LICENSE.txt for details.
from qt import QtCore, QtGui
import logging

logger = logging.getLogger(__name__)

class BaseTable(QtGui.QTableView):
    def __init__(self, parent):
        super(BaseTable, self).__init__(parent)
        self._context_items = []
        self.setupUi(self)

    def setupUi(self, w):
        pass

    @property
    def context_actions(self):
        return self._context_items

    def contextMenuEvent(self, event):
        actions = list(self.context_actions)
        if actions:
            menu = QtGui.QMenu(self)
            for action_or_menu in actions:
                if isinstance(action_or_menu, QtGui.QAction):
                    menu.addAction(action_or_menu)
                else:
                    menu.addMenu(action_or_menu)
            menu.exec_(event.globalPos())

class MasterTable(BaseTable):
    def setupUi(self, w):
        super(MasterTable, self).setupUi(w)
        self.action_cols = action = QtGui.QAction("&Columns", self)
        self._context_items.append(action)

class DetailTable(BaseTable):
    pass

class LoggerTree(QtGui.QTreeView):
    def contextMenuEvent(self, event):
        logger.debug('tree context event')
