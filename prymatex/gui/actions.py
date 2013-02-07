#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtCore, QtGui

from prymatex import resources
from prymatex.core import exceptions
from prymatex.models.selectable import selectableModelFactory
from prymatex.gui import dialogs
from prymatex.gui.dialogs.template import PMXNewFromTemplateDialog

from prymatex.utils.i18n import ugettext as _

class MainWindowActions(object):
    
    splitTabWidget = None #Overriden in GUI Setup
    
    def setupMenu(self):
        #Recent files
        self.actionFullscreen.setChecked(self.windowState() == QtCore.Qt.WindowFullScreen)
        self.actionShowStatus.setChecked(self.statusBar().isVisible())
        self.actionShowMenus.setChecked(self.menuBar().isVisible())
        
        #Bundles Menu
        self.application.supportManager.appendMenuToBundleMenuGroup(self.menuBundles)
        
    # ------------ About To Show Menus
    def on_menuRecentFiles_aboutToShow(self):
        self.menuRecentFiles.clear()
        for index, filePath in enumerate(self.application.fileManager.fileHistory, 1):
            actionText = "%s (%s)\t&%d" % (self.application.fileManager.basename(filePath), filePath, index)
            action = QtGui.QAction(actionText, self)
            receiver = lambda file = filePath: self.application.openFile(file)
            self.connect(action, QtCore.SIGNAL('triggered()'), receiver)
            self.menuRecentFiles.addAction(action)
        self.menuRecentFiles.addSeparator()
        self.menuRecentFiles.addAction(self.actionOpenAllRecentFiles)
        self.menuRecentFiles.addAction(self.actionRemoveAllRecentFiles)

    # ------------ File Actions
    @QtCore.pyqtSlot()
    def on_actionNewEditor_triggered(self):
        self.addEmptyEditor()

    @QtCore.pyqtSlot()
    def on_actionNewFromTemplate_triggered(self):
        filePath = PMXNewFromTemplateDialog.newFileFromTemplate(parent = self)

        if filePath:
            self.application.openFile(filePath)
    
    @QtCore.pyqtSlot()
    def on_actionNewProject_triggered(self):
        projectDialog = self.findChild(QtGui.QDialog, "ProjectDialog")
        projectDialog.createProject()

    @QtCore.pyqtSlot()
    def on_actionOpen_triggered(self):
        filePath = self.currentEditor().filePath if self.currentEditor() is not None else None
        files = dialogs.getOpenFiles(directory = self.application.fileManager.directory(filePath))
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
        directory = QtGui.QFileDialog.getExistingDirectory(self, "Choose project location", self.application.fileManager.directory())
        if directory:
            try:
                self.application.projectManager.importProject(directory)
            except exceptions.LocationIsNotProject:
                QtGui.QMessageBox.critical(self, "Critical", "A error has occurred.\n%s is not a valid project location." % directory)

    @QtCore.pyqtSlot()
    def on_actionSave_triggered(self):
        self.saveEditor()
        
    @QtCore.pyqtSlot()
    def on_actionSaveAs_triggered(self):
        self.saveEditor(saveAs = True)
        
    @QtCore.pyqtSlot()
    def on_actionSaveAll_triggered(self):
        for w in self.editors():
            self.saveEditor(editor = w)

    @QtCore.pyqtSlot()
    def on_actionClose_triggered(self):
        self.closeEditor()

    @QtCore.pyqtSlot()
    def on_actionCloseAll_triggered(self):
        for w in self.splitTabWidget.allWidgets():
            self.closeEditor(editor = w)

    @QtCore.pyqtSlot()
    def on_actionCloseOthers_triggered(self):
        current = self.currentEditor()
        for w in self.splitTabWidget.allWidgets():
            if w is not current:
                self.closeEditor(editor = w)
    
    @QtCore.pyqtSlot()
    def on_actionQuit_triggered(self):
        QtGui.QApplication.quit()
    
    @QtCore.pyqtSlot()
    def on_actionSwitchProfile_triggered(self):
        if self.profileDialog.switchProfile() == self.profileDialog.Accepted and\
            self.application.profileManager.defaultProfile() != self.application.currentProfile:
            self.application.restart()


    # ------------ Edit Actions
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
        
    # ------------ View Actions
    @QtCore.pyqtSlot()
    def on_actionZoomIn_triggered(self):
        if self.currentEditor() is not None:
            self.currentEditor().zoomIn()
            
    @QtCore.pyqtSlot()
    def on_actionZoomOut_triggered(self):
        if self.currentEditor() is not None:
            self.currentEditor().zoomOut()

    # ------------ Navigation Actions
    @QtCore.pyqtSlot()
    def on_actionNextTab_triggered(self):
        self.splitTabWidget.focusNextTab()

    @QtCore.pyqtSlot()
    def on_actionPreviousTab_triggered(self):
        self.splitTabWidget.focusPreviousTab()

    @QtCore.pyqtSlot()
    def on_actionSelectTab_triggered(self):
        item = self.selectorDialog.select(self.tabSelectableModel, title=_("Select tab"))
        
        if item is not None:
            self.splitTabWidget.setCurrentWidget(item['data'])
    
    @QtCore.pyqtSlot()
    def on_actionJumpToTabWindow_triggered(self):
        if self.currentEditor() is not None:
            self.currentEditor().setFocus()
    
    # ------------ Global navigation
    @QtCore.pyqtSlot()
    def on_actionLocationBack_triggered(self):
        if self._editorHistory and self._editorHistoryIndex < len(self._editorHistory) - 1:
            self._editorHistoryIndex += 1
            entry = self._editorHistory[self._editorHistoryIndex]
            if "memento" in entry:
                entry["editor"].restoreLocationMemento(entry["memento"])
            self.setCurrentEditor(entry["editor"])
        
    @QtCore.pyqtSlot()
    def on_actionLocationForward_triggered(self):
        if self._editorHistoryIndex != 0:
            self._editorHistoryIndex -= 1
            entry = self._editorHistory[self._editorHistoryIndex]
            if "memento" in entry:
                entry["editor"].restoreLocationMemento(entry["memento"])
            self.setCurrentEditor(entry["editor"])
    
    @QtCore.pyqtSlot()
    def on_actionLastEditLocation_triggered(self):
        for index, entry in enumerate(self._editorHistory):
            if "memento" in entry:
                entry["editor"].restoreLocationMemento(entry["memento"])
                self.setCurrentEditor(entry["editor"])
                self._editorHistoryIndex = index
                break

    # ------------ Bundles Actions
    @QtCore.pyqtSlot()
    def on_actionShowBundleEditor_triggered(self):
        self.bundleEditorDialog.execEditor()

    @QtCore.pyqtSlot()
    def on_actionEditCommands_triggered(self):
        self.bundleEditorDialog.execCommand()
    
    @QtCore.pyqtSlot()
    def on_actionEditLanguages_triggered(self):
        self.bundleEditorDialog.execLanguage()
    
    @QtCore.pyqtSlot()
    def on_actionEditSnippets_triggered(self):
        self.bundleEditorDialog.execSnippet()
        
    @QtCore.pyqtSlot()
    def on_actionReloadBundles_triggered(self):
        self.supportManager.reloadSupport(self.showMessage)

    # ------------ Preferences Actions
    @QtCore.pyqtSlot(bool)
    def on_actionShowMenus_toggled(self, checked):
        self.menuBar().setVisible(checked)
        
    @QtCore.pyqtSlot(bool)
    def on_actionShowStatus_toggled(self, checked):
        self.statusBar().setVisible(checked)
    
    @QtCore.pyqtSlot(bool)
    def on_actionFullscreen_toggled(self, checked):
        self.toggleDockToolBarVisibility()
        if checked:
            self.showFullScreen()
        else:
            self.showNormal()

    @QtCore.pyqtSlot()
    def on_actionSettings_triggered(self):
        self.settingsDialog.exec_()
            
    # ------------ Help Actions
    @QtCore.pyqtSlot()
    def on_actionAboutQt_triggered(self):
        QtGui.qApp.aboutQt()

    @QtCore.pyqtSlot()
    def on_actionAbout_triggered(self):
        self.aboutDialog.exec_()
        
    @QtCore.pyqtSlot()
    def on_actionProjectHomepage_triggered(self):
        import webbrowser
        import prymatex
        webbrowser.open(getattr(prymatex, '__url__', "https://github.com/prymatex/prymatex"))
    
    SCREENSHOT_FORMAT = 'png'
    
    @QtCore.pyqtSlot()
    def on_actionTakeScreenshot_triggered(self):
        pxm = QtGui.QPixmap.grabWindow(self.winId())
        import os
        from datetime import datetime
        now = datetime.now()
        baseName = now.strftime("%Y-%m-%d-%H_%M_%S") + '.' + self.SCREENSHOT_FORMAT
        path = os.path.join(self.application.profile.PMX_SCREENSHOT_PATH, baseName)
        pxm.save(path, self.SCREENSHOT_FORMAT)
        try:
            self.currentEditor().showMessage("%s saved" % baseName)
        except AttributeError as e:
            QtGui.QMessageBox.information(self, "Screenshoot", 
                "%s saved" % fileName)
        
    def setMainWindowAsActionParent(self):
        # Don't know if this brings side effects
        for name in (name for name in dir(self) if name.startswith('action')):
            obj = getattr(self, name)
            if not isinstance(obj, QtGui.QAction):
                continue
            #print "Making %s available when menubar is hidden %s" % (obj.objectName(), obj.text())
            self.addAction(obj)
    
    def setupHelpMenuMiscConnections(self):
        #self.actoin
        from webbrowser import open
        from functools import partial # Less code in simple callbacks :)
        import prymatex
        
        ACTION_MAPPING = {
                          self.actionReadDocumentation: prymatex.__source__ + '/wiki',
                          self.actionReportBug: 'https://github.com/prymatex/prymatex/issues?utf8=%E2%9C%93',
                          self.actionTranslatePrymatex: 'https://prymatex.com/translate',
                          self.actionProjectHomepage: prymatex.__url__
        }
        for action, url in ACTION_MAPPING.iteritems():
            action.triggered.connect(partial(open, url))
            
def tabSelectableModelFactory(mainWindow):
    """ 
    Shows select tab, and change to selected 
    """
    def dataFunction():
        return map(lambda tab: 
            dict(data = tab, 
                template = "<table><tr><td><h4>%(name)s</h4></td></tr><tr><td><small>%(file)s</small></td></tr></table>", 
                display = { "name": tab.tabTitle(), "file": tab.filePath }, 
                image = tab.tabIcon()) 
            ,mainWindow.splitTabWidget.allWidgets())

    return selectableModelFactory(mainWindow,
        dataFunction, filterFunction = lambda text, item: item["display"]["name"].find(text) != -1)
        
