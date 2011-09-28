# encoding: utf-8
'''
This module contains the main window status bar definition and widgets.
Some of the widgets defined here are:
    * The line counter
    * Syntax selector
    * 
'''
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import SIGNAL
from prymatex.core.base import PMXObject
from prymatex.utils.i18n import ugettext as _
from prymatex import resources

class PWMStatusLabel(QtGui.QLabel):
    '''
    A label which fires a menu when it's clicked. When an action is 
    '''
    valueChanged = QtCore.pyqtSignal(object)
    
    def __init__(self, text, parent, default = 0, *options):
        QtGui.QLabel.__init__(self, text, parent)
        self.setToolTip(text)
        self.menu = QtGui.QMenu(self)
        
        self.menu.triggered[QtGui.QAction].connect(self.indentModeChangedFromMenu)
        actions = []
        for name, value in options:
            action = self.menu.addAction(name)
            action.value = value
            actions.append(action)
        if actions:
            actions[default].trigger()
        
    def mouseReleaseEvent(self, event):
        if self.menu.actions():
            self.menu.popup( event.globalPos() ) #self.menu.exec_()
    
    def indentModeChangedFromMenu(self, action):
        self.setText(action.text())
        self.valueChanged.emit(action.value)

class PMXCursorPositionLabel(QtGui.QWidget):
    
    FORMAT = "Line: %5d Col: %5d"
    def __init__(self, parent):
        super(PMXCursorPositionLabel, self).__init__(parent)
        self.__text_format = self.trUtf8(self.FORMAT)
        layout = QtGui.QHBoxLayout()
        #self.label = QLabel(self.trUtf8('Pos:'))
        #layout.addWidget(self.label)
        self.postionLabel = QtGui.QLabel(self.text_format % (0, 0))
        fm = self.fontMetrics()
        self.postionLabel.setMinimumWidth(fm.width('0') * len(self.text_format) + 3 )
        layout.addWidget(self.postionLabel)
        self.setLayout(layout)

    @property
    def text_format(self):
        return unicode(self.__text_format)
        
    def update(self, col, line):
        self.postionLabel.setText(self.text_format % (line, col))

class PMXSymbolBox(QtGui.QComboBox):
    # TODO: Implement SymbolBox
    def __init__(self, parent):
        super(PMXSymbolBox, self).__init__(parent)        
            
class PMXStatusBar(QtGui.QStatusBar, PMXObject):
    '''
    Main Window status bar, declares some widgets
    '''
    syntaxChanged = QtCore.pyqtSignal(object)
    
    def __init__(self, parent):
        QtGui.QStatusBar.__init__(self, parent)
        
        self._widgetStatus = QtGui.QWidget()
        vbox = QtGui.QVBoxLayout(self._widgetStatus)
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.setSpacing(0)
        #Search Layout
        self._searchWidget = SearchWidget(self)
        vbox.addWidget(self._searchWidget)
        #Replace Layout
        self._replaceWidget = ReplaceWidget(self)
        vbox.addWidget(self._replaceWidget)
        #self._replaceWidget.setVisible(False)
        
        self.addWidget(self._widgetStatus)

        self._shortEsc = QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Escape), self)

        self.connect(self._searchWidget._btnClose, SIGNAL("clicked()"),
            self.hide_status)
        self.connect(self._searchWidget._btnFind, SIGNAL("clicked()"),
            self.find)
        self.connect(self._searchWidget.btnNext, SIGNAL("clicked()"),
            self.find_next)
        self.connect(self._searchWidget.btnPrevious, SIGNAL("clicked()"),
            self.find_previous)
        self.connect(self, SIGNAL("messageChanged(QString)"), self.message_end)
        self.connect(self._replaceWidget._btnCloseReplace, SIGNAL("clicked()"),
            lambda: self._replaceWidget.setVisible(False))
        self.connect(self._replaceWidget._btnReplace, SIGNAL("clicked()"),
            self.replace)
        self.connect(self._replaceWidget._btnReplaceAll, SIGNAL("clicked()"),
            self.replace_all)
        self.connect(self._shortEsc, SIGNAL("activated()"), self.hide_status)
        
        self.setupSyntaxMenu()
        
        #self.addWidget(self.lineColLabel)
        #self.addWidget(self.syntaxMenu)
        #self.addPermanentWidget(self.comboIndentMode)
        #self.addPermanentWidget(self.comboIndentWidth)
        
        self.connectSignals()
    
    def setCurrentEditor(self, editor):
        pass
    
    def setupSyntaxMenu(self):
        self.syntaxMenu = QtGui.QComboBox(self)
        tableView = QtGui.QTableView(self)
        tableView.setModel(self.application.supportManager.syntaxProxyModel)
        tableView.resizeColumnsToContents()
        tableView.resizeRowsToContents()
        tableView.verticalHeader().setVisible(False)
        tableView.horizontalHeader().setVisible(False)
        tableView.setShowGrid(False)
        tableView.setMinimumWidth(tableView.horizontalHeader().length() + 25)
        tableView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        tableView.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        tableView.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        tableView.setAutoScroll(False)
        self.syntaxMenu.setModel(self.application.supportManager.syntaxProxyModel);
        self.syntaxMenu.setModelColumn(0);
        self.syntaxMenu.setView(tableView);
    
    def mostrar(self, index):
        print self._combo.model()[index, 'item']
        print self._combo.model()[index, 'path']
    
    def setIndentMode(self, value):
        self.mainWindow.currentEditorWidget.codeEdit.softTabs = value 
    
    def setIndentWidth(self, value):
        self.warn("Tab Width %d" % value)
        self.mainWindow.currentEditorWidget.codeEdit.tabWidth = value
        
    def connectSignals(self):
        self.syntaxMenu.currentIndexChanged[int].connect(self.syntaxMenuIndexChanged)
    
    def syntaxMenuIndexChanged(self, index):
        model = self.syntaxMenu.model()
        node = model.mapToSource(model.createIndex(index, 0))
        syntax = node.internalPointer()
        self.syntaxChanged.emit(syntax)
        
    def updateStatus(self, status):
        self.lineColLabel.update(status['column'], status['line'])
    
    def updateSyntax(self, syntax):
        model =  self.syntaxMenu.model()
        index = model.findItemIndex(syntax)
        self.syntaxMenu.blockSignals(True)
        self.syntaxMenu.setCurrentIndex(index)
        self.syntaxMenu.blockSignals(False)
    
    def show(self):
        QStatusBar.show(self)
        if self._widgetStatus.isVisible():
            self._searchWidget._line.setFocus()
            self._searchWidget._line.selectAll()

    def show_replace(self):
        #self.show()
        #editor = main_container.MainContainer().get_actual_editor()
        #if editor:
        #    if editor.textCursor().hasSelection():
        #        word = editor.textCursor().selectedText()
        #        self._searchWidget._line.setText(word)
        #self._replaceWidget.setVisible(True)
        pass

    def show_with_word(self):
        #editor = main_container.MainContainer().get_actual_editor()
        #if editor:
        #    word = editor._text_under_cursor()
        #    self._searchWidget._line.setText(word)
        #    self.show()
        pass

    def hide_status(self):
        self._searchWidget._checkSensitive.setCheckState(Qt.Unchecked)
        self._searchWidget._checkWholeWord.setCheckState(Qt.Unchecked)
        self.hide()
        self._searchWidget.setVisible(True)
        self._replaceWidget.setVisible(False)
        #widget = self.mainWindowmain_container.MainContainer().get_actual_widget()
        #if widget:
        #    widget.setFocus()

    def replace(self):
        pass

    def replace_all(self):
        pass

    def find(self):
        pass

    def find_next(self):
        pass

    def find_previous(self):
        pass

    def showMessage(self, message, timeout):
        self._widgetStatus.hide()
        self._replaceWidget.setVisible(False)
        self.show()
        QStatusBar.showMessage(self, message, timeout)

    def message_end(self, message):
        if message == '':
            self.hide()
            QStatusBar.clearMessage(self)
            self._widgetStatus.show()
    
class SearchWidget(QtGui.QWidget):

    def __init__(self, parent):
        super(SearchWidget, self).__init__(parent)
        hSearch = QtGui.QHBoxLayout(self)
        hSearch.setContentsMargins(0, 0, 0, 0)
        self._line = TextLine(parent)
        self._line.setMinimumWidth(250)
        self._checkSensitive = QtGui.QCheckBox(self.tr("Respect Case Sensitive"))
        self._checkWholeWord = QtGui.QCheckBox(self.tr("Find Whole Words"))
        self._btnClose = QtGui.QPushButton(
            self.style().standardIcon(QtGui.QStyle.SP_DialogCloseButton), '')
        self._btnFind = QtGui.QPushButton(resources.ICONS['save'], '')
        self.btnPrevious = QtGui.QPushButton(
            self.style().standardIcon(QtGui.QStyle.SP_ArrowLeft), '')
        self.btnPrevious.setToolTip("Press (Ctrl + Left Arrow)")
        self.btnNext = QtGui.QPushButton(
            self.style().standardIcon(QtGui.QStyle.SP_ArrowRight), '')
        self.btnNext.setToolTip("Press (Ctrl + Right Arrow)")
        hSearch.addWidget(self._btnClose)
        hSearch.addWidget(self._line)
        hSearch.addWidget(self._btnFind)
        hSearch.addWidget(self.btnPrevious)
        hSearch.addWidget(self.btnNext)
        hSearch.addWidget(self._checkSensitive)
        hSearch.addWidget(self._checkWholeWord)


class ReplaceWidget(QtGui.QWidget):

    def __init__(self, parent):
        QtGui.QWidget.__init__(self, parent)
        hReplace = QtGui.QHBoxLayout(self)
        hReplace.setContentsMargins(0, 0, 0, 0)
        self._lineReplace = QtGui.QLineEdit()
        self._lineReplace.setMinimumWidth(250)
        self._btnCloseReplace = QtGui.QPushButton(
            self.style().standardIcon(QtGui.QStyle.SP_DialogCloseButton), '')
        self._btnReplace = QtGui.QPushButton(self.tr("Replace"))
        self._btnReplaceAll = QtGui.QPushButton(self.tr("Replace All"))
        hReplace.addWidget(self._btnCloseReplace)
        hReplace.addWidget(self._lineReplace)
        hReplace.addWidget(self._btnReplace)
        hReplace.addWidget(self._btnReplaceAll)

class TextLine(QtGui.QLineEdit):

    def __init__(self, parent):
        QtGui.QLineEdit.__init__(self, parent)
        self._parent = parent

    def keyPressEvent(self, event):
        editor = main_container.MainContainer().get_actual_editor()
        if editor and event.key() in \
        (QtCore.Qt.Key_Enter, QtCore.Qt.Key_Return):
            self._parent.find_next()
        elif event.modifiers() == Qt.ControlModifier and \
        event.key() == QtCore.Qt.Key_Right:
            self._parent.find_next()
            return
        elif event.modifiers() == Qt.ControlModifier and \
        event.key() == QtCore.Qt.Key_Left:
            self._parent.find_previous()
            return
        super(TextLine, self).keyPressEvent(event)
        if int(event.key()) in range(32, 162):
            self._parent.find()