#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtCore, QtGui
from prymatex.qt.compat import getOpenFileNames
from prymatex.qt.helpers import text2objectname, text_to_iconname, create_action

from prymatex import resources
from prymatex.core import exceptions
from prymatex.models.selectable import selectableModelFactory

from prymatex.utils.i18n import ugettext as _

class MainWindowActionsMixin(object):
    # -------------- Global callback for copy, paste cut...
    def globalCallback(self):
        """Global callback"""
        widget = self.application.focusWidget()
        action = self.sender()
        callback = action.data()
        getattr(widget, callback, lambda : None)()
        
    # ------------ About to show recent files
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

    # ------------ Update groups actions
    def on_splitter_layoutChanged(self):
        print("cambio el layout")
        for action in self.menuFocusGroup.actions()[3:]:
            self.menuFocusGroup.removeAction(action)
        for action in self.menuMoveEditorToGroup.actions()[3:]:
            self.menuMoveEditorToGroup.removeAction(action)
        for index, group in enumerate(self.centralWidget().allGroups(), 1):
            # TODO: Estos shortcuts no son configurables
            action = create_action(self, {
                "text": "Group %d" % index,
                "sequence": resources.get_sequence("Global", "Group %d" % index, "Ctrl+%d" % index).key(),
                "triggered": lambda group = group: self.setCurrentGroup(group)
            })
            self.menuFocusGroup.addAction(action)
            action = create_action(self, {
                "text": "Group %d" % index,
                "sequence": resources.get_sequence("Global", "Group %d" % index, "Shift+Ctrl+%d" % index).key(),
                "triggered": lambda group = group: self.moveEditorToGroup(group)
            })
            self.menuMoveEditorToGroup.addAction(action)

    # ------------ File Actions
    def on_actionOpen_triggered(self):
        current_editor = self.currentEditor()
        file_path = current_editor and current_editor.filePath() or None
        selected_paths, selected_filter = getOpenFileNames(
            self,
            caption="Open files",
            basedir=self.application.fileManager.directory(file_path)
        )
        for file_path in selected_paths:
            self.application.openFile(
                file_path,
                focus = selected_paths[-1] == file_path   # Focus on last editor
            )

    def on_actionImportProject_triggered(self):
        directory = QtGui.QFileDialog.getExistingDirectory(self, "Choose project location", self.application.fileManager.directory())
        if directory:
            try:
                self.application.projectManager.importProject(directory)
            except exceptions.LocationIsNotProject:
                QtGui.QMessageBox.critical(self, "Critical", "A error has occurred.\n%s is not a valid project location." % directory)

    def on_actionCloseOthers_triggered(self):
        current = self.currentEditor()
        for w in self.centralWidget().allWidgets():
            if w is not current:
                self.closeEditor(editor = w)

    def on_actionSwitchProfile_triggered(self):
        if self.profileDialog.switchProfile() == self.profileDialog.Accepted and\
            self.application.profileManager.defaultProfile() != self.application.currentProfile:
            self.application.restart()

    # ------------ Navigation Actions
    def on_actionSelectTab_triggered(self):
        item = self.selectorDialog.select(self.tabSelectableModel, title=_("Select tab"))

        if item is not None:
            self.centralWidget().setCurrentWidget(item['data'])

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
        import collections
        menu = collections.OrderedDict()

        # ------------- File menu
        menu["file"] = {
            "text": "&File",
            "items": [{
                "text": "New",
                "items": [{
                    "text": "Editor",
                    'sequence': resources.get_sequence("Global", "New"),
                    "triggered": cls.addEmptyEditor,
                    "icon": resources.get_icon("tab-new"),
                }, "-", {
                    "text": "From template",
                    "triggered": lambda mw: mw.templateDialog.createFile(),
                    "icon": resources.get_icon("document-new"),
                }, {
                    "text": "Project",
                    "triggered": lambda mw: mw.projectDialog.createProject(),
                    "icon": resources.get_icon("project-development-new-template"),
                }]
            }, {
                "text": "Open",
                'sequence': resources.get_sequence("Global", "Open"),
                "icon": resources.get_icon("document-open"),
                "triggered": cls.on_actionOpen_triggered
            }, {
                "text": "Recent files",
                "aboutToShow": cls.on_menuRecentFiles_aboutToShow,
                "items": ["-", {
                    "text": "Open all recent files",
                    "icon": resources.get_icon("document-open-recent"),
                    "triggered": lambda mw: [ mw.application.openFile(path)
                        for path in mw.application.fileManager.fileHistory ]
                }, {
                    "text": "Remove all recent files",
                    "icon": resources.get_icon("edit-clear"),
                    "triggered": lambda mw: mw.application.fileManager.clearFileHistory()
                }]
            }, {
                "text": "Import project",
                "triggered": cls.on_actionImportProject_triggered,
                "icon": resources.get_icon("project-open"),
            }, "-", {
                "text": "Save",
                'sequence': resources.get_sequence("Global", "Save"),
                "icon": resources.get_icon("document-save"),
                "triggered": lambda mw: mw.saveEditor()
            }, {
                "text": "Save as",
                "icon": resources.get_icon("document-save-as"),
                "triggered": lambda mw: mw.saveEditor(saveAs=True)
            }, {
                "text": "Save all",
                'sequence': resources.get_sequence("Global", "SaveAll", "Ctrl+Shift+S"),
                "icon": resources.get_icon("document-save-all"),
                "triggered": lambda mw: [ mw.saveEditor(editor=editor) for editor in mw.editors() ]
            }, "-", {
                "text": "Close",
                'sequence': resources.get_sequence("Global", "Close"),
                "icon": resources.get_icon("tab-close"),
                "triggered": lambda mw: mw.closeEditor()
            }, {
                "text": "Close all",
                'sequence': resources.get_sequence("Global", "CloseAll", "Ctrl+Shift+W"),
                "triggered": lambda mw: [ mw.closeEditor(editor=editor) for editor in mw.editors() ]
            }, {
                "text": "Close others",
                "icon": resources.get_icon("tab-close-other")
            }, "-", {
                "text": "Switch profile",
                "icon": resources.get_icon("system-switch-user"),
                "triggered": cls.on_actionSwitchProfile_triggered
            }, "-", {
                "text": "Quit",
                'sequence': resources.get_sequence("Global", "Quit"),
                "icon": resources.get_icon("application-exit"),
                "triggered": lambda mw: mw.application.quit()
            }]
        }

        # ------------- Edit menu
        def globalEditAction(text):
            objectName = text2objectname(text)
            iconName = text_to_iconname(text, prefix = "edit")
            return {
                "text": text,
                'sequence': resources.get_sequence("Global", objectName),
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
            }, "-", {
                "text": "Show main menu",
                "toggled": lambda mw, checked: mw.menuBar().setShown(checked),
                "testChecked": lambda mw: mw.menuBar().isVisible()
            }, {
                "text": "Show status",
                "toggled": lambda mw, checked: mw.statusBar().setShown(checked),
                "testChecked": lambda mw: mw.statusBar().isVisible()
            }, {
                "text": "Show tabs",
                "toggled": lambda mw, checked: mw.centralWidget().setShowTabs(checked),
                "testChecked": lambda mw: mw.centralWidget().showTabs(),
            }, "-", {
                "text": "Layout",
                "items": [{
                    "text": "Split vertically",
                    "icon": resources.get_icon("view-split-left-right"),
                    "triggered": lambda mw: mw.centralWidget().splitVertically()
                }, {
                    "text": "Split horizontally",
                    "icon": resources.get_icon("view-split-top-bottom"),
                    "triggered": lambda mw: mw.centralWidget().splitHorizontally()
                }, "-", {
                    "text": "Single",
                    "sequence": resources.get_sequence("Global", "LayoutSingle", "Shift+Alt+1"),
                    "triggered": lambda mw: mw.centralWidget().setLayout()
                }, {
                    "text": "Columns: 2",
                    "sequence": resources.get_sequence("Global", "Layout2Columns", "Shift+Alt+2"),
                    "triggered": lambda mw: mw.centralWidget().setLayout(columns = 2)
                }, {
                    "text": "Columns: 3",
                    "sequence": resources.get_sequence("Global", "Layout3Columns", "Shift+Alt+3"),
                    "triggered": lambda mw: mw.centralWidget().setLayout(columns = 3)
                }, {
                    "text": "Columns: 4",
                    "sequence": resources.get_sequence("Global", "Layout4Columns", "Shift+Alt+4"),
                    "triggered": lambda mw: mw.centralWidget().setLayout(columns = 4)
                }, {
                    "text": "Rows: 2",
                    "sequence": resources.get_sequence("Global", "Layout2Rows", "Shift+Alt+8"),
                    "triggered": lambda mw: mw.centralWidget().setLayout(rows = 2)
                }, {
                    "text": "Rows: 3",
                    "sequence": resources.get_sequence("Global", "Layout3Rows", "Shift+Alt+9"),
                    "triggered": lambda mw: mw.centralWidget().setLayout(rows = 3)
                }, {
                    "text": "Grid: 4",
                    "sequence": resources.get_sequence("Global", "Layout4Grid", "Shift+Alt+5"),
                    "triggered": lambda mw: mw.centralWidget().setLayout(columns = 2, rows = 2)
                }]
            }, {
                "text": "Groups",
                "items": [{
                    "text": "Move editor to new group",
                    "triggered": cls.moveEditorToNewGroup
                }, {
                    "text": "New group",
                    "triggered": cls.addEmptyGroup
                }, {
                    "text": "Close group",
                    "triggered": cls.closeGroup
                }, "-", {
                    "text": "Max Columns: 1",
                    "testChecked": lambda mw: mw.centralWidget().maxColumns() == 1,
                    "toggled": lambda mw, checked: checked and mw.centralWidget().setMaxColumns(1)
                }, {
                    "text": "Max Columns: 2",
                    "testChecked": lambda mw: mw.centralWidget().maxColumns() == 2,
                    "toggled": lambda mw, checked: checked and mw.centralWidget().setMaxColumns(2)
                }, {
                    "text": "Max Columns: 3",
                    "testChecked": lambda mw: mw.centralWidget().maxColumns() == 3,
                    "toggled": lambda mw, checked: checked and mw.centralWidget().setMaxColumns(3)
                }, {
                    "text": "Max Columns: 4",
                    "testChecked": lambda mw: mw.centralWidget().maxColumns() == 4,
                    "toggled": lambda mw, checked: checked and mw.centralWidget().setMaxColumns(4)
                }, {
                    "text": "Max Columns: 5",
                    "testChecked": lambda mw: mw.centralWidget().maxColumns() == 5,
                    "toggled": lambda mw, checked: checked and mw.centralWidget().setMaxColumns(5)
                }]
            }, {
                "text": "Focus group",
                "items": [{
                    "text": "Next",
                    "triggered": cls.nextGroup
                }, {
                    "text": "Previous",
                    "triggered": cls.previousGroup
                }, "-"]
            }, {
                "text": "Move editor to group",
                "items": [{
                    "text": "Next",
                    "triggered": cls.moveEditorToNextGroup
                }, {
                    "text": "Previous",
                    "triggered": cls.moveEditorToPreviousGroup
                }, "-"]
            }]
        }

        # ------------- Navigation menu
        menu["navigation"] = {
            "text": "Navigation",
            "items": [{
                "text": "Next tab",
                'sequence': resources.get_sequence("Global", "NextChild"),
                "icon": resources.get_icon("go-next-view"),
                "triggered": lambda mw: mw.centralWidget().focusNextTab()
            }, {
                "text": "Previous tab",
                'sequence': resources.get_sequence("Global", "PreviousChild"),
                "icon": resources.get_icon("go-previous-view"),
                "triggered": lambda mw: mw.centralWidget().focusPreviousTab()
            }, {
                "text": "Select tab",
                "triggered": cls.on_actionSelectTab_triggered
            }, {
                "text": "Jump to tab",
                'sequence': resources.get_sequence("Global", "JumpToTab", "F12"),
                "triggered": cls.on_actionJumpToTab_triggered
            }, "-", {
                "text": "Last edit location",
                "icon": resources.get_icon("go-last"),
                "triggered": cls.on_actionLastEditLocation_triggered
            }, {
                "text": "Go back location",
                'sequence': resources.get_sequence("Global", "GoBackLocation"),
                "icon": resources.get_icon("go-previous"),
                "triggered": cls.on_actionLocationBack_triggered
            }, {
                "text": "Go forward location",
                'sequence': resources.get_sequence("Global", "GoForwardLocation"),
                "icon": resources.get_icon("go-next"),
                "triggered": cls.on_actionLocationForward_triggered
            }]
        }

        # ------------- Bundles menu
        menu["bundles"] = {
            "text": "Bundles",
            "items": [{
                "text": "Bundle editor",
                "items": [{
                    "text": "Show bundle editor",
                    'sequence': resources.get_sequence("Global", "ShowBundleEditor", "Meta+Ctrl+Alt+B"),
                    "triggered": lambda mw: mw.bundleEditorDialog.execEditor()
                }, "-", {
                    "text": "Edit commands",
                    'sequence': resources.get_sequence("Global", "EditCommands", "Meta+Ctrl+Alt+C"),
                    "triggered": lambda mw: mw.bundleEditorDialog.execCommand()
                }, {
                    "text": "Edit languages",
                    'sequence': resources.get_sequence("Global", "EditLanguages", "Meta+Ctrl+Alt+L"),
                    "triggered": lambda mw: mw.bundleEditorDialog.execLanguage()
                }, {
                    "text": "Edit snippets",
                    'sequence': resources.get_sequence("Global", "EditSnippets", "Meta+Ctrl+Alt+S"),
                    "triggered": lambda mw: mw.bundleEditorDialog.execSnippet()
                }, {
                    "text": "Reload bundles",
                    "triggered": lambda mw: mw.application.supportManager.reloadSupport(mw.showMessage)
                }]
            }, "-"]
        }

        # ------------- Preferences menu
        menu["preferences"] = {
            "text": "&Preferences",
            "items": [ {
                "text": "Full screen",
                "toggled": lambda mw, checked: getattr(mw, checked and "showFullScreen" or "showNormal")(),
                "testChecked": lambda mw: mw.isFullScreen(),
                "icon": resources.get_icon("view-fullscreen"),
                "sequence": resources.get_sequence("Global", "ShowFullScreen", "F11")
            }, {
                "text": "Distraction free mode",
                "toggled": lambda mw, checked: getattr(mw, checked and "showDistractionFreeMode" or "showNormal")(),
                "sequence": resources.get_sequence("Global", "ShowDistractionFreeMode", "Shift+F11")
            }, "-", {
                "text": "Settings",
                "icon": resources.get_icon("configure"),
                "triggered": lambda mw: mw.settingsDialog.exec_()
            }]
        }

        # ------------- Help menu
        menu["help"] = {
            "text": "&Help",
            "items": [ {
                "text": "Read documentation",
                "icon": resources.get_icon("help-contents"),
                "triggered": lambda mw: mw.application.openUrl(prymatex.__source__ + '/wiki')
            }, {
                "text": "Project homepage",
                "triggered": lambda mw: mw.application.openUrl(prymatex.__url__)
            }, "-", {
                "text": "Translate Prymatex",
                "icon": resources.get_icon("applications-development-translation"),
                "triggered": lambda mw: mw.application.openUrl(prymatex.__source__ + '/wiki')
            }, "-", {
                "text": "Report bug",
                "icon": resources.get_icon("tools-report-bug"),
                "triggered": lambda mw: mw.application.openUrl(prymatex.__source__ + '/issues?utf8=%E2%9C%93')
            },  {
                "text": "Take screenshoot",
                "icon": resources.get_icon("ksnapshot"),
                "triggered": cls.on_actionTakeScreenshot_triggered
            }, "-", {
                "text": "About Prymatex",
                "triggered": lambda mw: mw.aboutDialog.exec_()
            }, {
                "text": "About Qt",
                "triggered": lambda mw: mw.application.aboutQt()
            }, ]
        }
        return menu

def tabSelectableModelFactory(mainWindow):
    """
    Shows select tab, and change to selected
    """
    def dataFunction():
        return [dict(data=tab,
                template="<table width='100%%'><tr><td><h4>%(name)s</h4></td></tr><tr><td><small>%(file)s</small></td></tr></table>",
                display={"name": tab.tabTitle(), "file": tab.filePath()},
                image=tab.tabIcon()) for tab in mainWindow.centralWidget().allWidgets()]

    return selectableModelFactory(
        mainWindow, dataFunction, 
        filterFunction=lambda text, item: \
            item["display"]["name"].find(text) != -1)
