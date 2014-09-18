#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtCore, QtGui, QtWidgets

from prymatex.delegates.items import HtmlItemDelegate
from prymatex.core.components import PMXBaseDialog
from prymatex.widgets.selector import SelectorWidget

class SelectorDialog(QtWidgets.QDialog, PMXBaseDialog):
    '''
    This dialog allow the user to search through commands, snippets and macros in the current scope easily.
    An instance is hold in the main window and triggered with an action.
    '''
    TIMEOUT_SORT = 2000
    def __init__(self, parent = None):
        QtGui.QDialog.__init__(self, parent)
        PMXBaseDialog.__init__(self)
        self.setupUi()
        self.model = None
        
        # Timer
        self.sortTimer = QtCore.QTimer(self)
        self.sortTimer.setSingleShot(True)
        
        # Event filter
        self.lineFilter.installEventFilter(self)
        self.listItems.installEventFilter(self)
        
        # Connect
        self.sortTimer.timeout.connect(self.on_sortTimer_timeout)
        self.listItems.activated.connect(self.on_listItems_triggered)
        self.listItems.doubleClicked.connect(self.on_listItems_triggered)
        self.lineFilter.returnPressed.connect(self.on_lineFilter_returnPressed)
        self.lineFilter.textChanged.connect(self.on_lineFilter_textChanged)
            
    def showEvent(self, event):
        # TODO Poner el widget en un lugar referente al widget que lo 
        # esta llamando o sobre el que se aplica
        QtWidgets.QDialog.showEvent(self, event)
        screen = self.application.desktop().screen()
        point = screen.rect().center() - self.rect().center()
        point.setY(point.y() * 0.5)
        self.move(point)
    
    def setupUi(self):
        self.setObjectName("SelectorDialog")
        self.verticalLayout = QtGui.QVBoxLayout(self)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lineFilter = QtGui.QLineEdit(self)
        self.lineFilter.setObjectName("lineFilter")
        self.lineFilter.setMinimumWidth(600)
        self.verticalLayout.addWidget(self.lineFilter)
        self.listItems = QtGui.QListView(self)
        self.listItems.setAlternatingRowColors(True)
        self.listItems.setUniformItemSizes(True)
        self.listItems.setObjectName("listItems")
        self.listItems.setItemDelegate(HtmlItemDelegate(self.listItems))
        self.verticalLayout.addWidget(self.listItems)
        # Popup
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.FramelessWindowHint)

    def setCurrentRow(self, row):
        index = self.model.index(0, row)
        #self.listItems.setVisible(index.isValid())
        self.listItems.setCurrentIndex(index)
        #self.listItems.resizeColumnsToContents()
        self.adjustSize()

    def setModel(self, model):
        if self.model != model:
            self.lineFilter.setVisible(model.isFilterable())
            if model.isFilterable():
                self.lineFilter.clear()
                self.lineFilter.setFocus()
            self.model = model
            self.listItems.setModel(self.model)
        else:
            self.lineFilter.clear()
            self.lineFilter.setFocus()
        self.setCurrentRow(0)

    def select(self, model, title = "Select item"):
        """ @param items: List of rows, each row has a list of columns, and each column is a dict with "title", "image", "tooltip"
            @return: The selected row """

        self.setWindowTitle(title)
        self.selected = None
        
        model.initialize(self)
        #self.setModel(model)
        self.completer = QtGui.QCompleter(model, self)
        self.completer.setCompletionMode(QtGui.QCompleter.PopupCompletion)
        self.lineFilter.setCompleter(self.completer)
        self.exec_()
        self.sortTimer.stop()
        
        return self.selected
    
    def eventFilter(self, obj, event):
        '''Filters lineEdit key strokes to select model items'''
        if obj is self.lineFilter:
            if event.type() == QtCore.QEvent.KeyPress:
                key = event.key() 
                if key == QtCore.Qt.Key_Down:
                    self.listItems.setFocus()
                    self.listItems.event(event)
                    obj.setFocus()
                    return True
                elif key == QtCore.Qt.Key_Up:
                    self.listItems.setFocus()
                    self.listItems.event(event)
                    obj.setFocus()
                    return True
        #elif obj is self.listItems:
        #    if event.type() == QtCore.QEvent.KeyPress:
        #        self.lineFilter.setFocus()
        #        self.lineFilter.event(event)
        #        return True
        return QtGui.QWidget.eventFilter(self, obj, event)

    # ------ Signals
    def on_sortTimer_timeout(self):
        self.model.sort(0)
        self.setCurrentRow(0)
    
    def on_listItems_triggered(self, index):
        self.selected = self.model.item(index)
        self.accept()

    def on_lineFilter_returnPressed(self):
        indexes = self.listItems.selectedIndexes()
        if indexes:
            self.on_listItems_triggered(indexes[0])

    # Not autoconnect, connect on model's needs
    def on_lineFilter_textChanged(self, text):
        self.completer.setCompletionPrefix(text)
        self.completer.complete()
        #self.model.setFilterString(text)
        #if self.model.isSortable() and not self.sortTimer.isActive():
        #    self.sortTimer.start(self.TIMEOUT_SORT)
        #else:
        #    self.setCurrentRow(0)

