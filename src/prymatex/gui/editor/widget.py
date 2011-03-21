'''
Code Editor Widget.
'''

from PyQt4.QtCore import SIGNAL, Qt, QString, pyqtSignal
from PyQt4.QtGui import QFont, QMessageBox, QFileDialog, QColor, QIcon, QWidget, \
    QAction, QMenu, QKeySequence, qApp

from logging import getLogger
from prymatex.bundles import PMXSyntax
from ui_editorwidget import Ui_EditorWidget
import logging
import os
import re
import sys
import traceback
from prymatex.core.filemanager import PMXFile
from prymatex.core.exceptions import APIUsageError


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

#===============================================================================
# Icons
#===============================================================================
ICON_FILE_STATUS_NORMAL = QIcon(qApp.instance().trUtf8(''
':/actions/resources/mimetypes/x-office-document.png'))
ICON_FILE_STATUS_MODIFIED = QIcon(qApp.instance().trUtf8(
':/actions/resources/actions/document-save-all.png'))

class PMXEditorWidget(QWidget, Ui_EditorWidget):
    '''
    It implements the logic needed for gui defined in ui_files/editorwidget.ui
    This logic includes Go To Line and Find action behaviour.
    '''
    
    COLOR_MODIFIED = QColor.fromRgb(0x81, 0x81, 0x81)
    COLOR_NORMAL = QColor("black")
    
    _counter = 0
    _time = None # Modification time
    __title = None
    _file = None
    
    fileTitleUpdate = pyqtSignal(PMXFile)
    
    def __init__(self, pmx_file):
        '''
        PMXEditorWidget instances gain Qt's parent attribute on PMXTabWidget.addTab() 
        '''
        super(PMXEditorWidget, self).__init__(None)
        
        self.setupActions()
        self.setupUi(self)
        
        self.setupFindReplaceWidget()
        
        self.codeEdit.addAction(self.actionFind)
        self.codeEdit.addAction(self.actionReplace)

        # Hide some widgets
        self.findreplaceWidget.hide()
        self.gotolineWidget.hide()
        
        self.file = pmx_file
        
    
    @property
    def file(self):
        return self._file
    
    @file.setter
    def file(self, file):
        if self._file is not None:
            raise APIUsageError("Can't set file twice")
        from prymatex.core.filemanager import PMXFile
        if not isinstance(file, PMXFile):
            raise APIUsageError("%s is not an instance of PMXFile" % file)
        self._file = file
        self._file.fileSaved.connect( self.fileSaved )
        
    
    def fileSaved(self):
        self.codeEdit.document().setModified(False)
        self.fileTitleUpdate.emit(self.file)
    
    # TODO: Move this thing up to tabwidget
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
    def getEditor(cls, pmx_file):
        '''
        Factory for the editors.
        PMXEditorWidget.registerEditor( editor )
        @param pmx_file: A PMXFile object, you can get it from qApp.instance().file_manager
        '''
        #TODO: Something with the pmx_file_instance
        from prymatex.core.filemanager import PMXFile
        if not isinstance(pmx_file, PMXFile):
            raise APIUsageError("%s is not a valid file" % pmx_file) 
        editor = PMXEditorWidget(pmx_file)
        return editor

    @classmethod
    def registerEditor(cls, editor_cls):
        '''
        Register an edior class.
        '''
        raise NotImplementedError("No implemented")

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

    def zoomIn(self):
        if self.codeEdit.font_size < self.codeEdit.MAX_FONT_POINT_SIZE:
            self.codeEdit.font_size += 1


    def zoomOut(self):
        if self.codeEdit.font_size > self.codeEdit.MIN_FONT_POINT_SIZE:
            self.codeEdit.font_size -= 1
            
    
    #===========================================================================
    # File Operations
    #===========================================================================
    def save(self):
        '''
        This method is call to actually save the file, the path has to be
        set.
        '''
        buffer_contents = unicode(self.codeEdit.document().toPlainText())
        #TODO: Check exceptions, for example, disk full.
        promise = self.file.write(buffer_contents)
        logger.debug("Buffer saved to %s" % self.file.path)
        
     
    
    def request_save(self, save_as = False):
        '''
        Save the document.
        do_save() actually saves the document, but it should no be called
        directly because it expects self.path to be defined.
        '''
        print "Save"
        from os.path import join
        print self.file.path
        if self.file.path is None or save_as:
            
            syntax = self.codeEdit.syntax
            save_path = unicode(qApp.instance().applicationDirPath())
            suggested_filename = self.file.suggestedFileName()
            
            
            if syntax:
                suffix = syntax.fileTypes[0]
                print "Suffix  is", suffix
                filetypes = '%s (%s)' % (syntax.name, ' '.join(["*.%s" % f for f in syntax.fileTypes]))
            else:
                filetypes = 'Text files (*.*)'
                suffix = None
                
            if save_as:
                suggested_filename = self.file.path
            else:
                suggested_filename = join(save_path, "%s.%s" % (suggested_filename, suffix))
            
            pth = QFileDialog.getSaveFileName(self, self.trUtf8("Save file"),
                                        suggested_filename,
                                        filetypes
                                        )
            if pth:
                self.file.path = pth
                
        self.save()

    
    def updateTitle(self):
        self.title = os.path.basename(self.path)
    
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

    def setSyntax(self):
        syntax = PMXSyntax.findSyntaxByFileType(self.path)
        self.codeEdit.setSyntax(syntax)
        
    @property
    def modfified(self):
        return self.codeEdit.document().isModified()
    
        
    #===========================================================================
    # Callbacks
    #===========================================================================
    
    def afterInsertion(self, tab_widget, index):
        ''' Callback when the tab is inserted '''
        tab_widget.setTabIcon(index, ICON_FILE_STATUS_NORMAL)
        # TODO: Settings tab's text should be made by the PMXTabWidget
        self.fileTitleUpdate.emit(self.file)
        #title = self.file.filename or self.file.suggestedFileName()
        #print title
        #tab_widget.setTabText(index, title)



if __name__ == "__main__":
    from PyQt4.QtGui import QApplication, QFont, QWidget, QVBoxLayout
    from PyQt4.QtGui import QPushButton
    app = QApplication(sys.argv)
    app.logger = {}
    win = PMXEditorWidget(None) # No Parent
    win.show()
    sys.exit(app.exec_())

