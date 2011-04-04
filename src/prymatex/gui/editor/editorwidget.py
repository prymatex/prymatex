#encoding: utf-8
'''
Code Editor Widget.
'''

from PyQt4.QtCore import SIGNAL, Qt, QString, pyqtSignal, QTimer
from PyQt4.QtGui import QFont, QMessageBox, QFileDialog, QColor, QIcon, QWidget, \
    QAction, QMenu, QKeySequence, qApp, QFocusEvent

from logging import getLogger
from prymatex.bundles import PMXSyntax
from ui_editorwidget import Ui_EditorWidget
import logging
import os
from os.path import join
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


class PMXEditorWidget(QWidget, Ui_EditorWidget):
    '''
    It implements the logic needed for gui defined in ui_files/editorwidget.ui
    This logic includes Go To Line and Find action behaviour.
    '''
    
    COLOR_MODIFIED = QColor.fromRgb(0x81, 0x81, 0x81)
    COLOR_NORMAL = QColor("black")
    
    _file = None
    
    #===========================================================================
    # Signals
    #===========================================================================
    fileTitleUpdate = pyqtSignal()
    fileStatusModified = pyqtSignal(object)
    fileStatusSynced = pyqtSignal(object)
    fileStatusOutOfSync = pyqtSignal(object)
    fileStatusDeleted = pyqtSignal(object)
    
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
        
        # TODO: Asyncronous I/O
        
        self.codeEdit.setPlainText(self.file.read() or '')
        self.destroyed.connect(self.releaseFile)
        
    def releaseFile(self):
        print "Release file"
        
    def focusInEvent(self, event):
        self.codeEdit.setFocus(Qt.MouseFocusReason)
    
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
        self.fileTitleUpdate.emit()
    
    # TODO: Move this thing up to tabwidget
    def on_codeEdit_modificationChanged(self, modified):
        if modified:
            self.fileStatusModified.emit(self)
        else:
            self.fileStatusSynced.emit(self)
            
    
    @property
    def tooltip(self):
        return self.tabwidget.tabToolTip(self.index)
    
    @tooltip.setter
    def tooltip(self, value):
        self.tabwidget.setTabToolTip(self.index, value)
    
    
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
    
    @property
    def modified(self):
        return self.codeEdit.document().isModified()
    
    #===========================================================================
    # Factory methods
    #===========================================================================
    
    @classmethod
    def editorFactory(cls, pmx_file):
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

    def request_close(self):
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
                return self.request_save()
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
        
    
    def propmpt_file(self, title = None):
        '''
        Prompts the user for a file name
        @return: filepath {unicode,str,QString} or None if the action is cancelled
        '''
        if not title:
            title = self.trUtf8("Save file...")
            
        syntax = self.codeEdit.syntax
        save_path = unicode(qApp.instance().startDirectory())
        suggested_filename = self.file.suggestedFileName()
        
        if syntax:
            suffix = syntax.fileTypes[0]
            filetypes = '%s (%s)' % (syntax.name, ' '.join(["*.%s" % f for f in syntax.fileTypes]))
        else:
            filetypes = 'Text files (*.*)'
            suffix = 'txt'
            
        if self.file.path:
            suggested_filename = self.file.path
        else:
            suggested_filename = join(save_path, suffix and "%s.%s" % (suggested_filename, 
                                                                        suffix) or suggested_filename)
        
        pth = QFileDialog.getSaveFileName( self, title, suggested_filename, filetypes )
        return pth
    
    def request_save(self, save_as = False):
        '''
        Saves the document asking the user for the required information.
        do_save() actually saves the document, but it should no be called
        directly because it expects self.path to be defined.
        @param save_as: Indicates filename has to be supplied
        '''
        title = self.trUtf8("Save file")
        if save_as:
            title = self.trUtf8("Save file as")
        if save_as or self.file.path is None:
            path = self.propmpt_file(title = title)
            if not path:
                logger.info("User cancelled save dialg")
                return False
            self.file.path = path
        self.save()
            


    def setSyntax(self):
        syntax = PMXSyntax.findSyntaxByFileType(self.path)
        self.codeEdit.setSyntax(syntax)
        
    @property
    def modfified(self):
        return self.codeEdit.document().isModified()
    
        
    #===========================================================================
    # Callbacks
    #===========================================================================
    
    def afterInsertionCallback(self):
        ''' Callback when the tab is inserted '''
        QTimer.singleShot(0, self.fileTitleUpdate.emit)
        # Does not work, signal is never emited :(
        #self.fileTitleUpdate.emit()
    
    def afterRemoveCallback(self):
        self.file.references -= 1


if __name__ == "__main__":
    from PyQt4.QtGui import QApplication, QFont, QWidget, QVBoxLayout
    from PyQt4.QtGui import QPushButton
    app = QApplication(sys.argv)
    app.logger = {}
    win = PMXEditorWidget(None) # No Parent
    win.show()
    sys.exit(app.exec_())

