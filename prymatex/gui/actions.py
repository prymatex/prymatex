#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtCore, QtGui
from prymatex.qt.compat import getOpenFileNames

from prymatex import resources
from prymatex.core import exceptions
from prymatex.models.selectable import selectableModelFactory

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
    @QtCore.Slot()
    def on_actionNewEditor_triggered(self):
        self.addEmptyEditor()

    @QtCore.Slot()
    def on_actionNewFromTemplate_triggered(self):
        filePath = self.templateDialog.createFile()

        if filePath:
            self.application.openFile(filePath)

    @QtCore.Slot()
    def on_actionNewProject_triggered(self):
        projectDialog = self.findChild(QtGui.QDialog, "ProjectDialog")
        projectDialog.createProject()

    @QtCore.Slot()
    def on_actionOpen_triggered(self):
        filePath = self.currentEditor().filePath if self.currentEditor() is not None else None
        filePaths, selectedfilter = getOpenFileNames(
            self, 
            caption = "Open files", 
            basedir = self.application.fileManager.directory(filePath)
            )
        focus = len(filePaths) == 1
        for filePath in filePaths:
            editor = self.application.openFile(filePath, focus = focus)

    @QtCore.Slot()
    def on_actionOpenAllRecentFiles_triggered(self):
        for filePath in self.application.fileManager.fileHistory:
            self.application.openFile(filePath)

    @QtCore.Slot()
    def on_actionRemoveAllRecentFiles_triggered(self):
        self.application.fileManager.clearFileHistory()

    @QtCore.Slot()
    def on_actionImportProject_triggered(self):
        directory = QtGui.QFileDialog.getExistingDirectory(self, "Choose project location", self.application.fileManager.directory())
        if directory:
            try:
                self.application.projectManager.importProject(directory)
            except exceptions.LocationIsNotProject:
                QtGui.QMessageBox.critical(self, "Critical", "A error has occurred.\n%s is not a valid project location." % directory)

    @QtCore.Slot()
    def on_actionSave_triggered(self):
        self.saveEditor()

    @QtCore.Slot()
    def on_actionSaveAs_triggered(self):
        self.saveEditor(saveAs = True)

    @QtCore.Slot()
    def on_actionSaveAll_triggered(self):
        for w in self.editors():
            self.saveEditor(editor = w)

    @QtCore.Slot()
    def on_actionClose_triggered(self):
        self.closeEditor()

    @QtCore.Slot()
    def on_actionCloseAll_triggered(self):
        for w in self.splitTabWidget.allWidgets():
            self.closeEditor(editor = w)

    @QtCore.Slot()
    def on_actionCloseOthers_triggered(self):
        current = self.currentEditor()
        for w in self.splitTabWidget.allWidgets():
            if w is not current:
                self.closeEditor(editor = w)
    
    @QtCore.Slot()
    def on_actionQuit_triggered(self):
        QtGui.QApplication.quit()
    
    @QtCore.Slot()
    def on_actionSwitchProfile_triggered(self):
        if self.profileDialog.switchProfile() == self.profileDialog.Accepted and\
            self.application.profileManager.defaultProfile() != self.application.currentProfile:
            self.application.restart()

    # ------------ Edit Actions
    @QtCore.Slot()
    def on_actionUndo_triggered(self):
        if self.currentEditor() is not None:
            self.currentEditor().undo()

    @QtCore.Slot()
    def on_actionRedo_triggered(self):
        if self.currentEditor() is not None:
            self.currentEditor().redo()
        
    @QtCore.Slot()
    def on_actionCopy_triggered(self):
        if self.currentEditor() is not None:
            self.currentEditor().copy()
    
    @QtCore.Slot()
    def on_actionCut_triggered(self):
        if self.currentEditor() is not None:
            self.currentEditor().cut()
        
    @QtCore.Slot()
    def on_actionPaste_triggered(self):
        if self.currentEditor() is not None:
            self.currentEditor().paste()

    @QtCore.Slot()
    def on_actionFind_triggered(self):
        self.statusBar().showIFind()

    @QtCore.Slot()
    def on_actionFindReplace_triggered(self):
        self.statusBar().showFindReplace()
        
    # ------------ View Actions
    @QtCore.Slot()
    def on_actionZoomIn_triggered(self):
        if self.currentEditor() is not None:
            self.currentEditor().zoomIn()
            
    @QtCore.Slot()
    def on_actionZoomOut_triggered(self):
        if self.currentEditor() is not None:
            self.currentEditor().zoomOut()

    # ------------ Navigation Actions
    @QtCore.Slot()
    def on_actionNextTab_triggered(self):
        self.splitTabWidget.focusNextTab()

    @QtCore.Slot()
    def on_actionPreviousTab_triggered(self):
        self.splitTabWidget.focusPreviousTab()

    @QtCore.Slot()
    def on_actionSelectTab_triggered(self):
        item = self.selectorDialog.select(self.tabSelectableModel, title=_("Select tab"))
        
        if item is not None:
            self.splitTabWidget.setCurrentWidget(item['data'])
    
    @QtCore.Slot()
    def on_actionJumpToTabWindow_triggered(self):
        if self.currentEditor() is not None:
            self.currentEditor().setFocus()
    
    # ------------ Global navigation
    @QtCore.Slot()
    def on_actionLocationBack_triggered(self):
        if self._editorHistory and self._editorHistoryIndex < len(self._editorHistory) - 1:
            self._editorHistoryIndex += 1
            entry = self._editorHistory[self._editorHistoryIndex]
            if "memento" in entry:
                entry["editor"].restoreLocationMemento(entry["memento"])
            self.setCurrentEditor(entry["editor"])
        
    @QtCore.Slot()
    def on_actionLocationForward_triggered(self):
        if self._editorHistoryIndex != 0:
            self._editorHistoryIndex -= 1
            entry = self._editorHistory[self._editorHistoryIndex]
            if "memento" in entry:
                entry["editor"].restoreLocationMemento(entry["memento"])
            self.setCurrentEditor(entry["editor"])
    
    @QtCore.Slot()
    def on_actionLastEditLocation_triggered(self):
        for index, entry in enumerate(self._editorHistory):
            if "memento" in entry:
                entry["editor"].restoreLocationMemento(entry["memento"])
                self.setCurrentEditor(entry["editor"])
                self._editorHistoryIndex = index
                break

    # ------------ Bundles Actions
    @QtCore.Slot()
    def on_actionShowBundleEditor_triggered(self):
        self.bundleEditorDialog.execEditor()

    @QtCore.Slot()
    def on_actionEditCommands_triggered(self):
        self.bundleEditorDialog.execCommand()
    
    @QtCore.Slot()
    def on_actionEditLanguages_triggered(self):
        self.bundleEditorDialog.execLanguage()
    
    @QtCore.Slot()
    def on_actionEditSnippets_triggered(self):
        self.bundleEditorDialog.execSnippet()
        
    @QtCore.Slot()
    def on_actionReloadBundles_triggered(self):
        self.application.supportManager.reloadSupport(self.showMessage)
        
    SCREENSHOT_FORMAT = 'png'
    
    def on_actionTakeScreenshot_triggered(self):
        pxm = QtGui.QPixmap.grabWindow(self.winId())
        import os
        from datetime import datetime
        now = datetime.now()
        baseName = now.strftime("%Y-%m-%d-%H_%M_%S") + '.' + self.SCREENSHOT_FORMAT
        path = os.path.join(self.application.currentProfile.PMX_SCREENSHOT_PATH, baseName)
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
    
    @classmethod
    def contributeToMainMenu(cls):
        import prymatex
        edit = {
            'text': '&Editor',
            "items": [{'text': 'Mode',
             'items': [
                {'text': 'Freehanded Editing', 'shortcut': 'Meta+Alt+E'},
                {'text': 'Overwrite Mode', 'shortcut': 'Meta+Alt+O'},
                {'text': 'Multi Edit Mode', 'shortcut': 'Meta+Alt+M'}
             ]}]
        }
        # ------------- Preferences menu
        preferences_menu = {
            "text": "&Preferences",
            "items": [{
                "text": "Show main menu",
                "toggled": lambda mainWindow, checked: mainWindow.menuBar().setShown(checked),
                "testChecked": lambda mainWindow: mainWindow.menuBar().isVisible()
            }, {
                "text": "Show status",
                "toggled": lambda mainWindow, checked: mainWindow.statusBar().setShown(checked),
                "testChecked": lambda mainWindow: mainWindow.statusBar().isVisible()
            }, "-", {
                "text": "Fullscreen",
                "toggled": lambda mainWindow, checked: getattr(mainWindow, checked and "showFullScreen" or "showNormal")(),
                "testChecked": lambda mainWindow: mainWindow.isFullScreen()
            }, "-", {
                "text": "Settings",
                "triggered": lambda mainWindow: mainWindow.settingsDialog.exec_()
            }]
        }
        # ------------- Help menu
        help_menu = {
            "text": "&Help",
            "items": [ {
                "text": "Report bug",
                "triggered": lambda mainWindow: mainWindow.application.openUrl(prymatex.__source__ + '/issues?utf8=%E2%9C%93')
            }, {
                "text": "Translate Prymatex",
                "triggered": lambda mainWindow: mainWindow.application.openUrl(prymatex.__source__ + '/wiki')
            }, {
                "text": "Project homepage",
                "triggered": lambda mainWindow: mainWindow.application.openUrl(prymatex.__url__)
            }, {
                "text": "Read documentation",
                "triggered": lambda mainWindow: mainWindow.application.openUrl(prymatex.__source__ + '/wiki')
            }, "-", {
                "text": "Take screenshoot",
                "icon": resources.get_icon("ksnapshot"),
                "triggered": cls.on_actionTakeScreenshot_triggered
            }, {
                "text": "About Qt",
                "triggered": lambda mainWindow: mainWindow.application.aboutQt()
            }, {
                "text": "About Prymatex",
                "triggered": lambda mainWindow: mainWindow.aboutDialog.exec_()
            }]
        }
        return { 
            "file": {},
            "edit": {},
            "view": {},
            "text": {},
            "navigation": {},
            "bundles": {},
            "preferences": preferences_menu,
            "help": help_menu
        }
    
def tabSelectableModelFactory(mainWindow):
    """ 
    Shows select tab, and change to selected 
    """
    def dataFunction():
        return [dict(data = tab, 
                template = "<table width='100%%'><tr><td><h4>%(name)s</h4></td></tr><tr><td><small>%(file)s</small></td></tr></table>", 
                display = { "name": tab.tabTitle(), "file": tab.filePath }, 
                image = tab.tabIcon()) for tab in mainWindow.splitTabWidget.allWidgets()]

    return selectableModelFactory(mainWindow,
        dataFunction, filterFunction = lambda text, item: item["display"]["name"].find(text) != -1)
