#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtCore, QtGui, QtWidgets
from prymatex.qt.compat import getOpenFileNames
from prymatex.qt.helpers import text_to_objectname, text_to_iconname, create_action

from prymatex.core import exceptions
from prymatex.models.selectable import selectableModelFactory

from prymatex.utils.i18n import ugettext as _

class MainWindowActionsMixin(object):
    # -------------- Global callback for copy, paste cut...
    def globalCallback(self, *args, **kwargs):
        """Global callback"""
        widget = self.application().focusWidget()
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
        for index, filePath in enumerate(self.application().fileManager.fileHistory, 1):
            action = create_action(self, {
                "text": "%s (%s)\t&%d" % (self.application().fileManager.basename(filePath), filePath, index),
                "triggered": lambda checked=False, file=filePath: self.application().openFile(file)
            })
            self.menuRecentFiles.addAction(action)
        self.menuRecentFiles.addActions(actions)

    # ------------ Update groups actions
    def on_splitter_layoutChanged(self):
        for action in self.menuFocusGroup.actions()[3:]:
            self.menuFocusGroup.removeAction(action)
        for action in self.menuMoveEditorToGroup.actions()[3:]:
            self.menuMoveEditorToGroup.removeAction(action)
        for index, group in enumerate(self.centralWidget().allGroups(), 1):
            # TODO: Estos shortcuts no son configurables
            action = create_action(self, {
                "text": "Group %d" % index,
                "sequence": ("Global", "Group %d" % index, "Ctrl+%d" % index),
                "triggered": lambda checked=False, group=group: self.setCurrentGroup(group)
            })
            self.menuFocusGroup.addAction(action)
            action = create_action(self, {
                "text": "Group %d" % index,
                "sequence": ("Global", "Group %d" % index, "Shift+Ctrl+%d" % index),
                "triggered": lambda checked=False, group=group: self.moveEditorToGroup(group)
            })
            self.menuMoveEditorToGroup.addAction(action)

    # ------------ File Actions
    def on_actionOpen_triggered(self, checked=False):
        current_editor = self.currentEditor()
        file_path = current_editor and current_editor.filePath() or None
        selected_paths, selected_filter = getOpenFileNames(
            self,
            caption="Open files",
            basedir=self.application().fileManager.directory(file_path)
        )
        for file_path in selected_paths:
            self.application().openFile(
                file_path,
                focus = selected_paths[-1] == file_path   # Focus on last editor
            )

    def on_actionImportProject_triggered(self, checked=False):
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, "Choose project location", self.application().fileManager.directory())
        if directory:
            try:
                self.application().projectManager.importProject(directory)
            except exceptions.LocationIsNotProject:
                QtWidgets.QMessageBox.critical(self, "Critical", "A error has occurred.\n%s is not a valid project location." % directory)

    def on_actionCloseOthers_triggered(self, checked=False):
        current = self.currentEditor()
        for w in self.centralWidget().allWidgets():
            if w is not current:
                self.closeEditor(editor = w)

    def on_actionSwitchProfile_triggered(self, checked=False):
        if self.profileDialog.switchProfile() == self.profileDialog.Accepted and\
            self.application().profileManager.defaultProfile() != self.application().profile():
            self.application().restart()

    # ------------ Navigation Actions
    def on_actionSelectTab_triggered(self, checked=False):
        item = self.selectorDialog.select(self.tabSelectableModel, title=_("Select tab"))

        if item is not None:
            self.centralWidget().setCurrentWidget(item['data'])

    def on_actionJumpToTab_triggered(self, checked=False):
        if self.currentEditor() is not None:
            self.currentEditor().setFocus()

    # ------------ Global navigation
    def on_actionLocationBack_triggered(self, checked=False):
        if self._editorHistory and self._editorHistoryIndex < len(self._editorHistory) - 1:
            self._editorHistoryIndex += 1
            entry = self._editorHistory[self._editorHistoryIndex]
            if "memento" in entry:
                entry["editor"].restoreLocationMemento(entry["memento"])
            self.setCurrentEditor(entry["editor"])

    def on_actionLocationForward_triggered(self, checked=False):
        if self._editorHistoryIndex != 0:
            self._editorHistoryIndex -= 1
            entry = self._editorHistory[self._editorHistoryIndex]
            if "memento" in entry:
                entry["editor"].restoreLocationMemento(entry["memento"])
            self.setCurrentEditor(entry["editor"])

    def on_actionLastEditLocation_triggered(self, checked=False):
        for index, entry in enumerate(self._editorHistory):
            if "memento" in entry:
                entry["editor"].restoreLocationMemento(entry["memento"])
                self.setCurrentEditor(entry["editor"])
                self._editorHistoryIndex = index
                break

    SCREENSHOT_FORMAT = 'png'

    def on_actionTakeScreenshot_triggered(self, checked=False):
        pxm = QtGui.QPixmap.grabWindow(self.winId())
        import os
        from datetime import datetime
        now = datetime.now()
        baseName = now.strftime("%Y-%m-%d-%H_%M_%S") + '.' + self.SCREENSHOT_FORMAT
        path = os.path.join(self.application().profile().PMX_SCREENSHOT_PATH, baseName)
        pxm.save(path, self.SCREENSHOT_FORMAT)
        try:
            self.showMessage("%s saved" % baseName)
        except AttributeError as e:
            QtWidgets.QMessageBox.information(self, "Screenshoot",
                "%s saved" % baseName)

    @classmethod
    def contributeToMainMenu(cls):
        import prymatex
        import collections
        menu = collections.OrderedDict()

        # ------------- File menu
        menu["file"] = {
            "text": "&File",
            "items": [{
                    "text": "New File",
                    "sequence": "New",
                    "triggered": lambda mw, checked=False: mw.addEmptyEditor(),
                    "icon": "new-editor",
                }, {
                    "text": "New From Template",
                    "triggered": lambda mw, checked=False: mw.templateDialog.createFile(),
                    "icon": "new-from-template",
                }, {
                    "text": "New Project",
                    "triggered": lambda mw, checked=False: mw.newProjectDialog.createProject(),
                    "icon": "new-project",
                }, "-", {
                    "text": "Open File",
                    "triggered": cls.on_actionOpen_triggered
                }, {
                    "text": "Recent Files",
                    "aboutToShow": cls.on_menuRecentFiles_aboutToShow,
                    "items": ["-", {
                        "text": "Open All Recent Files",
                        "triggered": lambda mw, checked=False: [ mw.application().openFile(path)
                            for path in mw.application().fileManager.fileHistory ]
                    }, {
                        "text": "Remove all recent files",
                        "triggered": lambda mw, checked=False: mw.application().fileManager.clearFileHistory()
                    }]
                }, {
                    "text": "Import Project",
                    "triggered": cls.on_actionImportProject_triggered,
                }, "-", {
                    "text": "Save",
                    "triggered": lambda mw, checked=False: mw.saveEditor()
                }, {
                    "text": "Save As",
                    "triggered": lambda mw, checked=False: mw.saveEditor(saveAs=True)
                }, {
                    "text": "Save All",
                    "sequence": ("Global", "SaveAll", "Ctrl+Shift+S"),
                    "triggered": lambda mw, checked=False: [ mw.saveEditor(editor=editor) for editor in mw.editors() ]
                }, "-", {
                    "text": "Close",
                    "triggered": lambda mw: mw.closeEditor()
                }, {
                    "text": "Close All",
                    "sequence": ("Global", "CloseAll", "Ctrl+Shift+W"),
                    "triggered": lambda mw: [ mw.closeEditor(editor=editor) for editor in mw.editors() ]
                }, {
                    "text": "Close Others",
                    "tirgger": cls.on_actionCloseOthers_triggered
                }, "-", {
                    "text": "Switch Profile",
                    "triggered": cls.on_actionSwitchProfile_triggered
                }, "-", {
                    "text": "Quit",
                    "triggered": lambda mw, checked=False: mw.application().quit()
                }
            ]
        }

        # ------------- Edit menu
        def globalEditAction(text):
            return {
                "text": text,
                "triggered": cls.globalCallback,
                "data": text_to_objectname(text)
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
                "text": "Show Main Menu",
                "checkable": True,
                "triggered": lambda mw, checked: mw.menuBar().setShown(checked),
                "testChecked": lambda mw: mw.menuBar().isVisible()
            }, {
                "text": "Show Status",
                "checkable": True,
                "triggered": lambda mw, checked: mw.statusBar().setShown(checked),
                "testChecked": lambda mw: mw.statusBar().isVisible()
            }, {
                "text": "Show Tabs",
                "checkable": True,
                "triggered": lambda mw, checked: mw.centralWidget().setShowTabs(checked),
                "testChecked": lambda mw: mw.centralWidget().showTabs(),
            }, "-", {
                "text": "Layout",
                "items": [{
                    "text": "Split Vertically",
                    "triggered": lambda mw, checked=False: mw.centralWidget().splitVertically()
                }, {
                    "text": "Split Horizontally",
                    "triggered": lambda mw, checked=False: mw.centralWidget().splitHorizontally()
                }, "-", {
                    "text": "Single",
                    "sequence": ("Global", "LayoutSingle", "Shift+Alt+1"),
                    "triggered": lambda mw, checked=False: mw.centralWidget().setLayout()
                }, {
                    "text": "Columns: 2",
                    "sequence": ("Global", "Layout2Columns", "Shift+Alt+2"),
                    "triggered": lambda mw, checked=False: mw.centralWidget().setLayout(columns = 2)
                }, {
                    "text": "Columns: 3",
                    "sequence": ("Global", "Layout3Columns", "Shift+Alt+3"),
                    "triggered": lambda mw, checked=False: mw.centralWidget().setLayout(columns = 3)
                }, {
                    "text": "Columns: 4",
                    "sequence": ("Global", "Layout4Columns", "Shift+Alt+4"),
                    "triggered": lambda mw, checked=False: mw.centralWidget().setLayout(columns = 4)
                }, {
                    "text": "Rows: 2",
                    "sequence": ("Global", "Layout2Rows", "Shift+Alt+8"),
                    "triggered": lambda mw, checked=False: mw.centralWidget().setLayout(rows = 2)
                }, {
                    "text": "Rows: 3",
                    "sequence": ("Global", "Layout3Rows", "Shift+Alt+9"),
                    "triggered": lambda mw, checked=False: mw.centralWidget().setLayout(rows = 3)
                }, {
                    "text": "Grid: 4",
                    "sequence": ("Global", "Layout4Grid", "Shift+Alt+5"),
                    "triggered": lambda mw, checked=False: mw.centralWidget().setLayout(columns = 2, rows = 2)
                }]
            }, {
                "text": "Groups",
                "items": [{
                    "text": "Move Editor to New Group",
                    "triggered": lambda mw, checked=False: mw.moveEditorToNewGroup()
                }, {
                    "text": "New Group",
                    "triggered": lambda mw, checked=False: mw.addEmptyGroup()
                }, {
                    "text": "Close Group",
                    "triggered": lambda mw, checked=False: mw.closeGroup()
                }, "-", {
                    "text": "Max Columns: 1",
                    "checkable": True,
                    "testChecked": lambda mw: mw.centralWidget().maxColumns() == 1,
                    "triggered": lambda mw, checked: checked and mw.centralWidget().setMaxColumns(1)
                }, {
                    "text": "Max Columns: 2",
                    "checkable": True,
                    "testChecked": lambda mw: mw.centralWidget().maxColumns() == 2,
                    "triggered": lambda mw, checked: checked and mw.centralWidget().setMaxColumns(2)
                }, {
                    "text": "Max Columns: 3",
                    "checkable": True,
                    "testChecked": lambda mw: mw.centralWidget().maxColumns() == 3,
                    "triggered": lambda mw, checked: checked and mw.centralWidget().setMaxColumns(3)
                }, {
                    "text": "Max Columns: 4",
                    "checkable": True,
                    "testChecked": lambda mw: mw.centralWidget().maxColumns() == 4,
                    "triggered": lambda mw, checked: checked and mw.centralWidget().setMaxColumns(4)
                }, {
                    "text": "Max Columns: 5",
                    "checkable": True,
                    "testChecked": lambda mw: mw.centralWidget().maxColumns() == 5,
                    "triggered": lambda mw, checked: checked and mw.centralWidget().setMaxColumns(5)
                }]
            }, {
                "text": "Focus group",
                "items": [{
                    "text": "Next",
                    "triggered": lambda mw, checked=False: mw.nextGroup()
                }, {
                    "text": "Previous",
                    "triggered": lambda mw, checked=False: mw.previousGroup()
                }, "-"]
            }, {
                "text": "Move editor to group",
                "items": [{
                    "text": "Next",
                    "triggered": lambda mw, checked=False: mw.moveEditorToNextGroup()
                }, {
                    "text": "Previous",
                    "triggered": lambda mw, checked=False: mw.moveEditorToPreviousGroup()
                }, "-"]
            }]
        }

        # ------------- Navigation menu
        menu["navigation"] = {
            "text": "&Navigation",
            "items": [{
                "text": "Next Tab",
                "sequence": "NextChild",
                "triggered": lambda mw: mw.centralWidget().focusNextTab()
            }, {
                "text": "Previous tab",
                "sequence": "PreviousChild",
                "triggered": lambda mw, checked=False: mw.centralWidget().focusPreviousTab()
            }, {
                "text": "Select Tab",
                "triggered": cls.on_actionSelectTab_triggered
            }, {
                "text": "Jump to Tab",
                "sequence": ("Global", "JumpToTab", "F12"),
                "triggered": cls.on_actionJumpToTab_triggered
            }, "-", {
                "text": "Last Edit Location",
                "triggered": cls.on_actionLastEditLocation_triggered
            }, {
                "text": "Go Back Location",
                "triggered": cls.on_actionLocationBack_triggered
            }, {
                "text": "Go Forward Location",
                "triggered": cls.on_actionLocationForward_triggered
            }]
        }

        # ------------- Bundles menu
        menu["bundles"] = {
            "text": "&Bundles",
            "items": [{
                "text": "Bundle Editor",
                "items": [{
                    "text": "Show Bundle Editor",
                    "sequence": ("Global", "ShowBundleEditor", "Meta+Ctrl+Alt+B"),
                    "triggered": lambda mw, checked=False: mw.bundleEditorDialog.execEditor()
                }, "-", {
                    "text": "Edit Commands",
                    "sequence": ("Global", "EditCommands", "Meta+Ctrl+Alt+C"),
                    "triggered": lambda mw, checked=False: mw.bundleEditorDialog.execCommand()
                }, {
                    "text": "Edit Languages",
                    "sequence": ("Global", "EditLanguages", "Meta+Ctrl+Alt+L"),
                    "triggered": lambda mw, checked=False: mw.bundleEditorDialog.execLanguage()
                }, {
                    "text": "Edit Snippets",
                    "sequence": ("Global", "EditSnippets", "Meta+Ctrl+Alt+S"),
                    "triggered": lambda mw, checked=False: mw.bundleEditorDialog.execSnippet()
                }, {
                    "text": "Reload Bundles",
                    "triggered": lambda mw, checked=False: mw.application().supportManager.reloadSupport(mw.showMessage)
                }]
            }, "-"]
        }

        # ------------- Preferences menu
        menu["preferences"] = {
            "text": "&Preferences",
            "items": [ {
                "text": "Full Screen",
                "checkable": True,
                "triggered": lambda mw, checked: getattr(mw, checked and "showFullScreen" or "showNormal")(),
                "testChecked": lambda mw: mw.isFullScreen(),
                "sequence": ("Global", "ShowFullScreen", "F11")
            }, {
                "text": "Distraction Free Mode",
                "checkable": True,
                "triggered": lambda mw, checked: getattr(mw, checked and "showDistractionFreeMode" or "showNormal")(),
                "sequence": ("Global", "ShowDistractionFreeMode", "Shift+F11")
            }, "-", {
                "text": "Settings - Dialog",
                "triggered": lambda mw, checked=False: mw.settingsDialog.exec_()
            }, {
                "text": "Settings - File",
                "triggered": lambda mw, checked=False: mw.application().openFile(
                    mw.profile().PMX_SETTINGS_PATH
                    )
            }]
        }

        # ------------- Help menu
        menu["help"] = {
            "text": "&Help",
            "items": [ {
                "text": "Read Documentation",
                "triggered": lambda mw, checked=False: mw.application().openUrl(prymatex.__source__ + '/wiki')
            }, {
                "text": "Project Homepage",
                "triggered": lambda mw, checked=False: mw.application().openUrl(prymatex.__url__)
            }, "-", {
                "text": "Translate Prymatex",
                "triggered": lambda mw, checked=False: mw.application().openUrl(prymatex.__source__ + '/wiki')
            }, "-", {
                "text": "Report Bug",
                "triggered": lambda mw, checked=False: mw.application().openUrl(prymatex.__source__ + '/issues?utf8=%E2%9C%93')
            },  {
                "text": "Take Screenshoot",
                "triggered": cls.on_actionTakeScreenshot_triggered
            }, "-", {
                "text": "About Prymatex",
                "triggered": lambda mw, checked=False: mw.aboutDialog.exec_()
            }, {
                "text": "About Qt",
                "triggered": lambda mw, checked=False: mw.application().aboutQt()
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
                display={"name": tab.title(), "file": tab.filePath()},
                image=tab.icon()) for tab in mainWindow.centralWidget().allWidgets()]

    return selectableModelFactory(
        mainWindow, dataFunction, 
        filterFunction=lambda text, item: \
            item["display"]["name"].find(text) != -1)
