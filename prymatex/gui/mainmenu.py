#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtCore, QtGui
from prymatex.qt.compat import getOpenFileNames
from prymatex.qt.helpers import text2objectname, text2iconname, create_action

from prymatex import resources
from prymatex.core import exceptions
from prymatex.core.components import PMXBaseComponent
from prymatex.models.selectable import selectableModelFactory

from prymatex.utils.i18n import ugettext as _

class MainMenuMixin(object):

    splitTabWidget = None #Overriden in GUI Setup

    # ------------ About To Show Menus
    def on_menuRecentFiles_aboutToShow(self):
        actions = self.menuRecentFiles.actions()[-3:]
        # TODO Algo mejor para no estar creando y matando actions como bestia
        for action in self.menuRecentFiles.actions():
            if action not in actions:
                self.menuRecentFiles.removeAction(action)
        for index, filePath in enumerate(self.application.fileManager.fileHistory, 1):
            action = create_action(self, {
                "text": "%s (%s)\t&%d" % (self.application.fileManager.basename(filePath), filePath, index),
                "triggered": lambda file = filePath: self.application.openFile(file)
            })
            self.menuRecentFiles.addAction(action)
        self.menuRecentFiles.addActions(actions)

    # ------------ File Actions
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

    def on_actionImportProject_triggered(self):
        directory = QtGui.QFileDialog.getExistingDirectory(self, "Choose project location", self.application.fileManager.directory())
        if directory:
            try:
                self.application.projectManager.importProject(directory)
            except exceptions.LocationIsNotProject:
                QtGui.QMessageBox.critical(self, "Critical", "A error has occurred.\n%s is not a valid project location." % directory)

    def on_actionCloseOthers_triggered(self):
        current = self.currentEditor()
        for w in self.splitTabWidget.allWidgets():
            if w is not current:
                self.closeEditor(editor = w)

    def on_actionSwitchProfile_triggered(self):
        if self.profileDialog.switchProfile() == self.profileDialog.Accepted and\
            self.application.profileManager.defaultProfile() != self.application.currentProfile:
            self.application.restart()

    # ------------ Navigation Actions
    def on_actionNextTab_triggered(self):
        self.splitTabWidget.focusNextTab()

    def on_actionPreviousTab_triggered(self):
        self.splitTabWidget.focusPreviousTab()

    def on_actionSelectTab_triggered(self):
        item = self.selectorDialog.select(self.tabSelectableModel, title=_("Select tab"))

        if item is not None:
            self.splitTabWidget.setCurrentWidget(item['data'])

    def on_actionJumpToTab_triggered(self):
        if self.currentEditor() is not None:
            self.currentEditor().setFocus()

    # ------------ Global navigation
    def on_actionLocationBack_triggered(self):
        if self._editorHistory and self._editorHistoryIndex < len(self._editorHistory) - 1:
            self._editorHistoryIndex += 1
            entry = self._editorHistory[self._editorHistoryIndex]
            if "memento" in entry:
                entry["editor"].restoreLocationMemento(entry["memento"])
            self.setCurrentEditor(entry["editor"])

    def on_actionLocationForward_triggered(self):
        if self._editorHistoryIndex != 0:
            self._editorHistoryIndex -= 1
            entry = self._editorHistory[self._editorHistoryIndex]
            if "memento" in entry:
                entry["editor"].restoreLocationMemento(entry["memento"])
            self.setCurrentEditor(entry["editor"])

    def on_actionLastEditLocation_triggered(self):
        for index, entry in enumerate(self._editorHistory):
            if "memento" in entry:
                entry["editor"].restoreLocationMemento(entry["memento"])
                self.setCurrentEditor(entry["editor"])
                self._editorHistoryIndex = index
                break

    SCREENSHOT_FORMAT = 'png'

    def on_actionTakeScreenshot_triggered(self):
        # TODO Mas moderno esto, que ya esta muy viejo
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

    @classmethod
    def contributeToMainMenu(cls):
        import prymatex
        menu = PMXBaseComponent.contributeToMainMenu()
        menu["file"] = {
            "text": "&File",
            "items": [{
                "text": "New",
                "items": [{
                    "text": "Editor",
                    "shortcut": resources.get_shortcut("_", "New"),
                    "triggered": lambda mainWindow: mainWindow.addEmptyEditor(),
                    "icon": resources.get_icon("tab-new"),
                }, "-", {
                    "text": "From template",
                    "triggered": lambda mainWindow: mainWindow.templateDialog.createFile(),
                    "icon": resources.get_icon("document-new"),
                }, {
                    "text": "Project",
                    "triggered": lambda mainWindow: mainWindow.projectDialog.createProject(),
                    "icon": resources.get_icon("project-development-new-template"),
                }]
            }, {
                "text": "Open",
                "shortcut": resources.get_shortcut("_", "Open"),
                "icon": resources.get_icon("document-open"),
                "triggered": cls.on_actionOpen_triggered
            }, {
                "text": "Recent files",
                "aboutToShow": cls.on_menuRecentFiles_aboutToShow,
                "items": ["-", {
                    "text": "Open all recent files",
                    "icon": resources.get_icon("document-open-recent"),
                    "triggered": lambda mainWindow: [ mainWindow.application.openFile(path)
                        for path in mainWindow.application.fileManager.fileHistory ]
                }, {
                    "text": "Remove all recent files",
                    "icon": resources.get_icon("edit-clear"),
                    "triggered": lambda mainWindow: mainWindow.application.fileManager.clearFileHistory()
                }]
            }, {
                "text": "Import project",
                "triggered": cls.on_actionImportProject_triggered,
                "icon": resources.get_icon("project-open"),
            }, "-", {
                "text": "Save",
                "shortcut": resources.get_shortcut("_", "Save"),
                "icon": resources.get_icon("document-save"),
                "triggered": lambda mainWindow: mainWindow.saveEditor()
            }, {
                "text": "Save as",
                "icon": resources.get_icon("document-save-as"),
                "triggered": lambda mainWindow: mainWindow.saveEditor(saveAs = True)
            }, {
                "text": "Save all",
                "icon": resources.get_icon("document-save-all"),
                "triggered": lambda mainWindow: [ mainWindow.saveEditor(editor = editor) for editor in self.editors() ]
            }, "-", {
                "text": "Close",
                "shortcut": resources.get_shortcut("_", "Close"),
                "icon": resources.get_icon("tab-close"),
                "triggered": lambda mainWindow: mainWindow.closeEditor()
            }, {
                "text": "Close all",
                "triggered": lambda mainWindow: [ mainWindow.closeEditor(editor = editor) for editor in self.editors() ]
            }, {
                "text": "Close others",
                "icon": resources.get_icon("tab-close-other")
            }, "-", {
                "text": "Switch profile",
                "icon": resources.get_icon("system-switch-user")
            }, "-", {
                "text": "Quit",
                "shortcut": resources.get_shortcut("_", "Quit"),
                "icon": resources.get_icon("application-exit"),
                "triggered": lambda mainWindow: mainWindow.application.quit()
            }]
        }

        # ------------- Edit menu
        def globalEditAction(text):
            objectName = text2objectname(text)
            iconName = text2iconname(text, prefix = "edit")
            return {
                "text": text,
                "shortcut": resources.get_shortcut("_", objectName),
                "icon": resources.get_icon(iconName),
                "triggered": cls.globalCallback,
                "data": objectName
            }
        menu["edit"] = {
            "text": "&Edit",
            "items": [ globalEditAction(name) for name in ("&Undo", "&Redo") ] + ["-"] +
            [ globalEditAction(name) for name in ("Cu&t", "&Copy", "&Paste", "&Delete") ]
        }
        # ------------- View menu
        menu["view"] = {
            "text": "&View",
            "items": [{
                "text": "Panels",
                "items": []
            }]

        }

        # ------------- Navigation menu
        menu["navigation"] = {
            "text": "Navigation",
            "items": [{
                "text": "Next tab",
                "shortcut": resources.get_shortcut("_", "NextChild"),
                "icon": resources.get_icon("go-next-view"),
                "triggered": cls.on_actionNextTab_triggered
            }, {
                "text": "Previous tab",
                "shortcut": resources.get_shortcut("_", "PreviousChild"),
                "icon": resources.get_icon("go-previous-view"),
                "triggered": cls.on_actionPreviousTab_triggered
            }, {
                "text": "Select tab",
                "triggered": cls.on_actionSelectTab_triggered
            }, {
                "text": "Jump to tab",
                "shortcut": resources.get_shortcut("_", "JumpToTab", "F12"),
                "triggered": cls.on_actionJumpToTab_triggered
            }, "-", {
                "text": "Last edit location",
                "icon": resources.get_icon("go-last"),
                "triggered": cls.on_actionPreviousTab_triggered
            }, {
                "text": "Go back location",
                "shortcut": resources.get_shortcut("_", "GoBackLocation"),
                "icon": resources.get_icon("go-previous"),
                "triggered": cls.on_actionPreviousTab_triggered
            }, {
                "text": "Go forward location",
                "shortcut": resources.get_shortcut("_", "GoForwardLocation"),
                "icon": resources.get_icon("go-next"),
                "triggered": cls.on_actionPreviousTab_triggered
            }]
        }

        # ------------- Bundles menu
        menu["bundles"] = {
            "text": "Bundles",
            "items": [{
                "text": "Bundle editor",
                "items": [{
                    "text": "Show bundle editor",
                    "shortcut": resources.get_shortcut("_", "ShowBundleEditor", "Meta+Ctrl+Alt+B"),
                    "triggered": lambda mainWindow: mainWindow.bundleEditorDialog.execEditor()
                }, "-", {
                    "text": "Edit commands",
                    "shortcut": resources.get_shortcut("_", "ShowBundleEditor", "Meta+Ctrl+Alt+C"),
                    "triggered": lambda mainWindow: mainWindow.bundleEditorDialog.execCommand()
                }, {
                    "text": "Edit languages",
                    "shortcut": resources.get_shortcut("_", "ShowBundleEditor", "Meta+Ctrl+Alt+L"),
                    "triggered": lambda mainWindow: mainWindow.bundleEditorDialog.execLanguage()
                }, {
                    "text": "Edit snippets",
                    "shortcut": resources.get_shortcut("_", "ShowBundleEditor", "Meta+Ctrl+Alt+S"),
                    "triggered": lambda mainWindow: mainWindow.bundleEditorDialog.execSnippet()
                }, {
                    "text": "Reload bundles",
                    "triggered": lambda mainWindow: mainWindow.application.supportManager.reloadSupport(mainWindow.showMessage)
                }]
            }, "-"]
        }

        # ------------- Preferences menu
        menu["preferences"] = {
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
        menu["help"] = {
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
        return menu

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
