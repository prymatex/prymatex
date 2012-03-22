#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui

from prymatex import resources
from prymatex.gui import dialogs
from prymatex.gui.dialogs.newfromtemplate import PMXNewFromTemplateDialog
from prymatex.gui.dialogs.newproject import PMXNewProjectDialog
from prymatex.gui.about import PMXAboutDialog

class MainWindowActions(object):
    
    splitTabWidget = None #Overriden in GUI Setup
    
    def setupMenu(self):
        #Recent files
        self.actionFullscreen.setChecked(self.windowState() == QtCore.Qt.WindowFullScreen)
        self.actionShowStatus.setChecked(self.statusBar().isVisible())
        self.actionShowMenus.setChecked(self.menuBar().isVisible())
        
        #Bundles Menu
        self.application.supportManager.appendMenuToBundleMenuGroup(self.menuBundles)
        
    #============================================================
    # About To Show Menus
    #============================================================
    def on_menuRecentFiles_aboutToShow(self):
        self.menuRecentFiles.clear()
        for index, filePath in enumerate(self.application.fileManager.fileHistory, 1):
            actionText = "%s (%s)\t&%d" % (self.application.fileManager.fileName(filePath), filePath, index)
            action = QtGui.QAction(actionText, self)
            receiver = lambda file = filePath: self.application.openFile(file)
            self.connect(action, QtCore.SIGNAL('triggered()'), receiver)
            self.menuRecentFiles.addAction(action)
        self.menuRecentFiles.addSeparator()
        self.menuRecentFiles.addAction(self.actionOpenAllRecentFiles)
        self.menuRecentFiles.addAction(self.actionRemoveAllRecentFiles)

    #============================================================
    # File Actions
    #============================================================
    @QtCore.pyqtSlot()
    def on_actionNewEditor_triggered(self):
        self.addEmptyEditor()

    @QtCore.pyqtSlot()
    def on_actionNewFileFromTemplate_triggered(self):
        filePath = PMXNewFromTemplateDialog.newFileFromTemplate(parent = self)

        if filePath:
            self.application.openFile(filePath)
    
    @QtCore.pyqtSlot()
    def on_actionNewProject_triggered(self):
        PMXNewProjectDialog.getNewProject(self)

    @QtCore.pyqtSlot()
    def on_actionOpen_triggered(self):
        filePath = self.currentEditor().filePath if self.currentEditor() is not None else None
        files = dialogs.getOpenFiles(directory = self.application.fileManager.getDirectory(filePath))
        focus = len(files) == 1
        for filePath in files:
            editor = self.application.openFile(filePath, focus = focus)
    
    @QtCore.pyqtSlot()
    def on_actionOpenAllRecentFiles_triggered(self):
        for filePath in self.application.fileManager.fileHistory:
            self.application.openFile(filePath)

    @QtCore.pyqtSlot()
    def on_actionRemoveAllRecentFiles_triggered(self):
        self.application.fileManager.clearFileHistory()

    @QtCore.pyqtSlot()
    def on_actionImportProject_triggered(self):
        directory = QtGui.QFileDialog.getExistingDirectory(self, "Choose project location", self.application.fileManager.getDirectory())
        if directory:
            self.application.projectManager.importProject(directory)
        
    @QtCore.pyqtSlot()
    def on_actionSave_triggered(self):
        self.saveEditor()
        
    @QtCore.pyqtSlot()
    def on_actionSaveAs_triggered(self):
        self.saveEditor(saveAs = True)
        
    @QtCore.pyqtSlot()
    def on_actionSaveAll_triggered(self):
        for w in self.splitTabWidget.getAllWidgets():
            self.saveEditor(editor = w)

    @QtCore.pyqtSlot()
    def on_actionClose_triggered(self):
        self.closeEditor()

    @QtCore.pyqtSlot()
    def on_actionCloseAll_triggered(self):
        for w in self.splitTabWidget.getAllWidgets():
            self.closeEditor(editor = w)

    @QtCore.pyqtSlot()
    def on_actionCloseOthers_triggered(self):
        current = self.currentEditor()
        for w in self.splitTabWidget.getAllWidgets():
            if w is not current:
                self.closeEditor(editor = w)
    
    @QtCore.pyqtSlot()
    def on_actionQuit_triggered(self):
        QtGui.QApplication.quit()
    
    #============================================================
    # Edit Actions
    #============================================================
    @QtCore.pyqtSlot()
    def on_actionUndo_triggered(self):
        if self.currentEditor() is not None:
            self.currentEditor().undo()

    @QtCore.pyqtSlot()
    def on_actionRedo_triggered(self):
        if self.currentEditor() is not None:
            self.currentEditor().redo()
        
    @QtCore.pyqtSlot()
    def on_actionCopy_triggered(self):
        if self.currentEditor() is not None:
            self.currentEditor().copy()
    
    @QtCore.pyqtSlot()
    def on_actionCut_triggered(self):
        if self.currentEditor() is not None:
            self.currentEditor().cut()
        
    @QtCore.pyqtSlot()
    def on_actionPaste_triggered(self):
        if self.currentEditor() is not None:
            self.currentEditor().paste()

    @QtCore.pyqtSlot()
    def on_actionFind_triggered(self):
        self.statusBar().showIFind()

    @QtCore.pyqtSlot()
    def on_actionFindReplace_triggered(self):
        self.statusBar().showFindReplace()
        
    #============================================================
    # View Actions
    #============================================================
    @QtCore.pyqtSlot()
    def on_actionZoomIn_triggered(self):
        if self.currentEditor() is not None:
            self.currentEditor().zoomIn()
            
    @QtCore.pyqtSlot()
    def on_actionZoomOut_triggered(self):
        if self.currentEditor() is not None:
            self.currentEditor().zoomOut()

    #============================================================
    # Navigation Actions
    #============================================================
    @QtCore.pyqtSlot()
    def on_actionNextTab_triggered(self):
        self.splitTabWidget.focusNextTab()

    @QtCore.pyqtSlot()
    def on_actionPreviousTab_triggered(self):
        self.splitTabWidget.focusPreviousTab()

    @QtCore.pyqtSlot()
    def on_actionSelectTab_triggered(self):
        """ 
        Shows select tab, and change to selected 
        """
        tabs = self.splitTabWidget.getAllWidgets()
        def tabsToDict(tabs):
            for tab in tabs:
                image = tab.tabIcon()
                if image is None: image = QtGui.QIcon()
                yield [ dict(title = tab.tabTitle(), image = image), dict(title = tab.filePath) ]
        index = self.tabSelectorDialog.select(tabsToDict(tabs))
        if index is not None:
            tab = tabs[index]
            self.splitTabWidget.setCurrentWidget(tab)
            
    #============================================================
    # Bundles Actions
    #============================================================
    @QtCore.pyqtSlot()
    def on_actionShowBundleEditor_triggered(self):
        #TODO: mejorar esto
        self.application.bundleEditor.execEditor()

    @QtCore.pyqtSlot()
    def on_actionEditCommands_triggered(self):
        #TODO: mejorar esto
        self.application.bundleEditor.execCommand()
    
    @QtCore.pyqtSlot()
    def on_actionEditLanguages_triggered(self):
        #TODO: mejorar esto
        self.application.bundleEditor.execLanguage()
    
    @QtCore.pyqtSlot()
    def on_actionEditSnippets_triggered(self):
        #TODO: mejorar esto
        self.application.bundleEditor.execSnippet()
        
    @QtCore.pyqtSlot()
    def on_actionReloadBundles_triggered(self):
        editor = self.currentEditor()
        self.application.supportManager.reloadSupport(editor.showMessage)

    #============================================================
    # Preferences Actions
    #============================================================
    @QtCore.pyqtSlot(bool)
    def on_actionShowMenus_toggled(self, checked):
        self.menuBar().setVisible(checked)
        
    @QtCore.pyqtSlot(bool)
    def on_actionShowStatus_toggled(self, checked):
        self.statusBar().setVisible(checked)
    
    @QtCore.pyqtSlot(bool)
    def on_actionFullscreen_toggled(self, checked):
        if checked:
            self.showFullScreen()
        else:
            self.showNormal()

    @QtCore.pyqtSlot()
    def on_actionSettings_triggered(self):
        self.application.settingsDialog.exec_()
            
    #============================================================
    # Help Actions
    #============================================================
    @QtCore.pyqtSlot()
    def on_actionAbout_Qt_triggered(self):
        QtGui.qApp.aboutQt()

    aboutDialog = None
            
    @QtCore.pyqtSlot()
    def on_actionAbout_triggered(self):
        # Lazy 
        if not self.aboutDialog:
            self.aboutDialog = PMXAboutDialog(self) 
        self.aboutDialog.exec_()
        
    @QtCore.pyqtSlot()
    def on_actionProjectHomepage_triggered(self):
        import webbrowser
        import prymatex
        url = getattr(prymatex, '__url__', "https://github.com/D3f0/prymatex")
        webbrowser.open(url)
    
    SCREENSHOT_FORMAT = 'png'
    
    @QtCore.pyqtSlot()
    def on_actionTakeScreenshot_triggered(self):
        pxm = QtGui.QPixmap.grabWindow(self.winId())
        from datetime import datetime
        now = datetime.now()
        fileName = now.strftime("sshot-%Y-%m-%d-%H_%M_%S") + '.' + self.SCREENSHOT_FORMAT
        pxm.save(fileName, self.SCREENSHOT_FORMAT)
        try:
            self.currentEditor().showMessage("%s saved" % fileName)
        except AttributeError as e:
            QtGui.QMessageBox.information(self, "Screenshoot", 
                "%s saved" % fileName)
            
        