'''
'''
from PyQt4.QtGui import QWidget, QAction, QMenu, QKeySequence, qApp
from PyQt4.QtGui import QFont, QMessageBox, QFileDialog, QColor,QIcon
from PyQt4.QtCore import SIGNAL, Qt, QString
from logging import getLogger
import sys
import traceback
import re
import os
import logging

#from prymatex.lib.deco import logresult
logger = logging.getLogger(__name__)

# Path correction for standalone test
if __name__ == "__main__":
    from os.path import abspath, join, dirname
    pmx_base = abspath(join(dirname(__file__), '..', '..', '..'))
    sys.path.append(pmx_base)
    sys.path.append('../..')
    #pmx_base = abspath(join(dirname(__file__), '..', '..', '..'))

# Qt Designer's gui
from ui_editorwidget import Ui_EditorWidget

#===============================================================================
# Icons
#===============================================================================
ICON_FILE_STATUS_NORMAL = QIcon(qApp.instance().trUtf8(''
':/actions/resources/mimetypes/x-office-document.png'))
ICON_FILE_STATUS_MODIFIED = QIcon(qApp.instance().trUtf8(
':/actions/resources/actions/document-save-all.png'))

class PMXEditorWidget(QWidget, Ui_EditorWidget):
    _counter = 0
    _time = None # Modification time
    __path = None
    __title = None
    
    def __init__(self, parent, path = None):
        from prymatex.gui.tabwidget import PMXTabWidget
        assert isinstance(parent, PMXTabWidget), "PMXEditorWidget can only be"\
                                                 " used with PMXTabWidget as"\
                                                 " parent."
        super(PMXEditorWidget, self).__init__(parent)
        
        self.setupActions()
        self.setupUi(self)
        
        self.setupFindReplaceWidget()
        #self.findreplaceWidget.hide()
        self.codeEdit.setFont(QFont("Monospace", 10))

        self.codeEdit.addAction(self.actionFind)
        self.codeEdit.addAction(self.actionReplace)
        
        self.findreplaceWidget.hide()
        
        if path:
            self.open(path)
            
        
    COLOR_MODIFIED = QColor.fromRgb(0x81, 0x81, 0x81)
    COLOR_NORMAL = QColor("black")
    
    def on_codeEdit_modificationChanged(self, modified):
        if modified:
            self.tooltip = self.trUtf8("Modified")
            self.tabwidget.setTabIcon(self.index, ICON_FILE_STATUS_MODIFIED)
            self.setTabTextColor(self.COLOR_MODIFIED)
        else:
            self.tooltip = self.trUtf8("")
            self.tabwidget.setTabIcon(self.index, ICON_FILE_STATUS_NORMAL)
            self.setTabTextColor(self.COLOR_NORMAL)
    
    @property
    def tooltip(self):
        return self.tabwidget.tabToolTip(self.index)
    
    @tooltip.setter
    def tooltip(self, value):
        self.tabwidget.setTabToolTip(self.index, value)
    
    @property
    def path(self):
        return self.__path
    
    @path.setter
    def path(self, value):
        if isinstance(value, (basestring, QString)):
            self.__path = unicode(value)
        elif value is None:
            self.__path = None
        else:
            raise ValueError("Path can't be a %s" % type(value))
        
        
    @property
    def title(self):
        if not self.__title:
            count = self.counter()
            if not count:
                self.__title = unicode(self.trUtf8("Untitled file"))
            else: 
                self.__title = unicode(self.trUtf8("Untitled file (%d)")) % count
        return  self.__title
    
    @title.setter
    def title(self, value):
        self.__title = value
        self.tabwidget.SetTabTitle(self.index, value)
    
    @property
    def index(self):
        return self.parent().indexOf(self)
    
    @property
    def tabwidget(self):
        # This is very ugly :(
        from prymatex.gui.tabwidget import PMXTabWidget
        w = self.parent()
        while not isinstance(w, PMXTabWidget):
            w = w.parent()
        return w
        
    def setTabTextColor(self, color):
        self.tabwidget.tabBar().setTabTextColor(self.index, color)
        
    @title.setter
    def title(self, value):
        self.__title = value
        self.tabwidget.setTabText(self.index, self.title)
         
    
    #===========================================================================
    # Factory methods
    #===========================================================================
    
    @classmethod
    def getEditor(cls, parent,  path = None):
        '''
        Factory for the default text editor
        '''
        from prymatex.gui.tabwidget import PMXTabWidget
        assert isinstance(parent, PMXTabWidget), cls.trUtf8("You didn't pass a valid parent: %s" % parent)
        editor = PMXEditorWidget(parent, path)
        return editor

    @classmethod
    def registerEditor(cls, editor_cls):
        '''
        Register an edior class.
        
        '''
        pass

    @classmethod
    def counter(cls):
        '''
        An infinite incremental counter to name untitled files
        '''
        v = cls._counter
        cls._counter += 1
        return v
        

    def setupActions(self):
        # Search
        self.actionFind = QAction("&Find", self)
        self.actionFind.setObjectName("actionFind")
        
        #self.actionFind.setShortcut(QKeySequence(self.trUtf8("Ctrl+F")))
        # Replace
        self.actionReplace = QAction(self.trUtf8("Find and &Replce"), self)
        self.actionReplace.setObjectName("actionReplace")
        #self.actionReplace.setShortcut(QKeySequence(self.trUtf8("Ctrl+R")))



    
    def on_actionFind_triggered(self):
        self.hideReplaceWidgets()
        self.findreplaceWidget.show()
        self.comboFind.setFocus(Qt.MouseFocusReason)


    def on_actionReplace_triggered(self):
        self.showReplaceWidgets()
        self.findreplaceWidget.show()
        self.comboFind.setFocus(Qt.MouseFocusReason)
        


    #TODO: @diego Too complex? Would it be better to make it more explicit?
    @property
    def replaceWidgets(self):
        return map(lambda name: getattr(self, name), ("labelReplaceWith", "comboReplace",
                                                      "pushReplaceAndFindPrevious",
                                                      "pushReplaceAndFindNext",
                                                      "pushReplaceAll"))
    def hideReplaceWidgets(self):
        map(lambda w: w.hide(), self.replaceWidgets)

    def showReplaceWidgets(self):
        map(lambda w: w.show(), self.replaceWidgets)

        
    def setupFindReplaceWidget(self):
        self.actionRegex = QAction(self.trUtf8("Use &regular expressions"),self)
        self.actionRegex.setCheckable(True)
        
        self.actionWholeWord = QAction(self.trUtf8("Find &whole word only"), self)
        self.actionWholeWord.setCheckable(True)

        self.actionCaseSensitive = QAction(self.trUtf8("Case &Sensitive"), self)
        self.actionCaseSensitive.setCheckable(True)

        self.menuOptions = QMenu()
        self.menuOptions.addAction(self.actionRegex)
        self.menuOptions.addAction(self.actionWholeWord)
        self.menuOptions.addAction(self.actionCaseSensitive)

        self.pushOptions.setMenu(self.menuOptions)

    def on_pushCloseFindreplace_pressed(self):
        self.findreplaceWidget.hide()

    def requestClose(self):
        '''
        When a editor has to be closed this method is called
        @returns true when it's safe to remove the editor wdiget, the user has been prompted
        for save
        '''
        doc = self.codeEdit.document()
        if doc.isModified():
            r = QMessageBox.question(self, self.trUtf8("Save changes?"), 
                                     self.trUtf8("Save changes for this file"),
                                     QMessageBox.Save | QMessageBox.Cancel | QMessageBox.No,
                                     QMessageBox.Cancel)
            
            if r == QMessageBox.Save:
                return self.save()
            elif r == QMessageBox.Cancel:
                return False
            elif r == QMessageBox.No:
                return True # Can close, discard changes
        return True

    MAX_POINT_SIZE = 24
    MIN_POINT_SIZE = 6

    def zoomIn(self):
        font = self.codeEdit.font()
        pt_size = font.pointSize()
        if pt_size < self.MAX_POINT_SIZE:
            pt_size += 1
            font.setPointSize(pt_size)
            logger.debug("Font size is now %d points", pt_size)
        self.codeEdit.setFont(font)

    def zoomOut(self):
        font = self.codeEdit.font()
        pt_size = font.pointSize()
        if pt_size > self.MIN_POINT_SIZE:
            pt_size -=  1
            font.setPointSize(pt_size)
            logger.debug("Font size is now %d points", pt_size)
        self.codeEdit.setFont(font)
    
    #===========================================================================
    # File Operations
    #===========================================================================
    def do_save(self):
        '''
        This method is call to actually save the file, the path has to be
        set.
        '''
        assert self.path is not None, self.trUtf8("No path defined!")
        print "File is: %s (%s)" % (self.path, type(self.path))
        buffer_contents = unicode(self.codeEdit.document().toPlainText())
        f = open(str(self.path), 'w')
        #TODO: Check exceptions, for example, disk full.
        n = f.write(buffer_contents)
        f.close()
        self.codeEdit.document().setModified(False)
        self.update_title()
        return n
     
    
    def save(self):
        '''
        Save the document.
        do_save() actually saves the document, but it should no be called
        directly because it expects self.path to be defined.
        '''
        if self.path:
            return self.do_save()
        else:
            path = QFileDialog.getSaveFileName(self,
                                                self.trUtf8("Save file as..."))
            if path:
                self.path = path
                return self.do_save()
        return False
    
    def update_title(self):
        self.title = os.path.basename(self.path)
    
    def open(self, path):
        '''
        Read file contents
        '''
        self.path = path
        self.readFileContents()
        self.update_title()
        # Maybe emit a signal?
    
    READ_SIZE = 1024 * 64 # 64K
    def readFileContents(self):
        '''
        Reads file contents
        '''
        self.codeEdit.setEnabled(False)
        self.codeEdit.clear()
        try:
            size, read_count = os.path.getsize(self.path), 0
            assert size > 0
        except OSError:
            logger.debug("Could not open %s", self.path)
        except AssertionError:
            logger.debug("Empty file")
        else:
            self.codeEdit.document().setUndoRedoEnabled(False)
            f = open(self.path, 'r')
            while size > read_count :
                content = f.read(self.READ_SIZE)
                read_count += len(content)
                self.codeEdit.insertPlainText(content)
                #logger.debug("%d bytes read_count from %s", read_count, self.path)
            f.close()
            self.codeEdit.document().setModified(False)
            self.codeEdit.document().setUndoRedoEnabled(True)
        self.codeEdit.setEnabled(True)
    
    def writeBufferContents(self):
        '''
        Writes contents from the buffer into the file specified by
        self.path
        '''
        raise NotImplementedError()

    @property
    def modfified(self):
        return self.codeEdit.document().isModified()
        
    #===========================================================================
    # Callbacks
    #===========================================================================
    
    def afterInsertion(self, tab_widget, index):
        ''' Callback when the tab is inserted '''
        tab_widget.setTabText(index, self.title)
        tab_widget.setTabIcon(index, ICON_FILE_STATUS_NORMAL)



if __name__ == "__main__":
    from PyQt4.QtGui import QApplication, QFont, QWidget, QVBoxLayout
    from PyQt4.QtGui import QPushButton
    app = QApplication(sys.argv)
    app.logger = {}
    win = PMXEditorWidget(None) # No Parent
    win.show()
    sys.exit(app.exec_())
   