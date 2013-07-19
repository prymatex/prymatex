#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ast
from pprint import pformat

from prymatex.qt import QtCore, QtGui

from prymatex import resources

from prymatex.ui.support.snippet import Ui_Snippet
from prymatex.ui.support.command import Ui_Command
from prymatex.ui.support.template import Ui_Template
from prymatex.ui.support.dragcommand import Ui_DragCommand
from prymatex.ui.support.language import Ui_Language
from prymatex.ui.support.bundle import Ui_Menu
from prymatex.ui.support.templatefile import Ui_TemplateFile
from prymatex.ui.support.preference import Ui_Preference
from prymatex.ui.support.macro import Ui_Macro
from prymatex.ui.support.project import Ui_Project
from prymatex.models.support import BundleItemMenuTreeModel

TABWIDTH = 20

class BundleItemEditorBaseWidget(QtGui.QWidget):
    '''Base class for editors'''
    TYPE = ''

    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        #The bundle item
        self.bundleItem = None
        self.changes = {}
        self.__title = 'No item selected'
        
    def isChanged(self):
        return self.bundleItem.hasChanged(self.changes)
    
    def title(self):
        return self.__title
    
    def getName(self):
        return self.changes.get('name', None)
    
    def setName(self, value):
        self.changes['name'] = value
    
    def getScope(self):
        return  self.changes.get('scope', None)
    
    def setScope(self, value):
        self.changes['scope'] = value

    def getTabTrigger(self):
        return self.changes.get('tabTrigger', None)
    
    def setTabTrigger(self, value):
        self.changes['tabTrigger'] = value
    
    def getKeyEquivalent(self):
        return self.changes.get('keyEquivalent', None)
    
    def setKeyEquivalent(self, value):
        self.changes['keyEquivalent'] = value
    
    def getSemanticClass(self):
        return self.changes.get('semanticClass', None)
    
    def setSemanticClass(self, value):
        self.changes['semanticClass'] = value

    def edit(self, bundleItem):
        self.bundleItem = bundleItem
        self.__title = bundleItem and 'Edit %s: "%s"' % (self.TYPE, bundleItem.name) or 'No item selected'
        self.changes = bundleItem and bundleItem.dump(includeNone = True) or {}

#============================================================
# None Widget
#============================================================
class NoneEditorWidget(BundleItemEditorBaseWidget):
    def __init__(self, parent = None):
        BundleItemEditorBaseWidget.__init__(self, parent)
        self.setupUi(self)

    def isChanged(self):
        return False
        
    def setupUi(self, widget):
        widget.setObjectName("NoneWidget")
        self.gridLayout = QtGui.QGridLayout(widget)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtGui.QLabel(widget)
        self.label.setEnabled(False)
        self.label.setText("")
        self.label.setPixmap(resources.getImage("prymo"))
        self.label.setScaledContents(True)
        self.label.setObjectName("labelPrymo")
        self.gridLayout.addWidget(self.label, 1, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 2, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 2, 1, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 0, 1, 1, 1)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem3, 1, 0, 1, 1)

#============================================================
# Snippet Editor Widget
#============================================================
class SnippetEditorWidget(BundleItemEditorBaseWidget, Ui_Snippet):
    TYPE = 'snippet'

    def __init__(self, parent = None):
        BundleItemEditorBaseWidget.__init__(self, parent)
        self.setupUi(self)
        self.content.setTabStopWidth(TABWIDTH)

    @QtCore.Slot()
    def on_content_textChanged(self):
        self.changes['content'] = self.content.toPlainText()
    
    def getScope(self):
        return super(SnippetEditorWidget, self).getScope() or ""
    
    def getTabTrigger(self):
        return super(SnippetEditorWidget, self).getTabTrigger() or ""
    
    def getKeyEquivalent(self):
        return super(SnippetEditorWidget, self).getKeyEquivalent() or ""
    
    def edit(self, bundleItem):
        super(SnippetEditorWidget, self).edit(bundleItem)
        self.content.setPlainText(self.changes["content"])

class CommandEditorWidget(BundleItemEditorBaseWidget, Ui_Command):
    TYPE = 'command'
    
    def __init__(self, parent = None):
        BundleItemEditorBaseWidget.__init__(self, parent)
        self.setupUi(self)
        self.comboBoxBeforeRunning.addItem("Nothing", "nop")
        self.comboBoxBeforeRunning.addItem("Current File", "saveActiveFile")
        self.comboBoxBeforeRunning.addItem("All Files in Project", "saveModifiedFiles")
        self.comboBoxBeforeRunning.currentIndexChanged[int].connect(self.on_comboBoxBeforeRunning_changed)
        
        self.comboBoxInput.addItem("None", "none")
        self.comboBoxInput.addItem("Selected Text", "selection") #selectedText
        self.comboBoxInput.addItem("Entire Document", "document")
        self.comboBoxInput.currentIndexChanged[int].connect(self.on_comboBoxInput_changed)
        
        self.comboBoxFallbackInput.addItem("Document", "document")
        self.comboBoxFallbackInput.addItem("Line", "line")
        self.comboBoxFallbackInput.addItem("Word", "word")
        self.comboBoxFallbackInput.addItem("Character", "character")
        self.comboBoxFallbackInput.addItem("Scope", "scope")
        self.comboBoxFallbackInput.addItem("Nothing", "none")
        self.comboBoxFallbackInput.currentIndexChanged[int].connect(self.on_comboBoxFallbackInput_changed)
        
        self.comboBoxInputFormat.addItem("Text", "text")
        self.comboBoxInputFormat.addItem("XML", "xml")
        self.comboBoxInputFormat.currentIndexChanged[int].connect(self.on_comboBoxInputFormat_changed)
        
        self.comboBoxOutput.addItem("Discard", "discard")
        self.comboBoxOutput.addItem("Replace Selected Text", "replaceSelectedText")
        self.comboBoxOutput.addItem("Replace Document", "replaceDocument")
        self.comboBoxOutput.addItem("Insert as Text", "insertText")
        self.comboBoxOutput.addItem("Insert as Snippet", "insertAsSnippet")
        self.comboBoxOutput.addItem("Show as HTML", "showAsHTML")
        self.comboBoxOutput.addItem("Show as Tool Tip", "showAsTooltip")
        self.comboBoxOutput.addItem("Create New Document", "createNewDocument")
        self.comboBoxOutput.addItem("Open as New Document", "openAsNewDocument")
        self.comboBoxOutput.addItem("Open as New Window", "newWindow")
        self.comboBoxOutput.currentIndexChanged[int].connect(self.on_comboBoxOutput_changed)
        
        self.comboBoxOutputFormat.addItem("Text", "text")
        self.comboBoxOutputFormat.addItem("Html", "html")
        self.comboBoxOutputFormat.currentIndexChanged[int].connect(self.on_comboBoxOutputFormat_changed)
        
        self.comboBoxCaret.addItem("After Output", "afterOutput")
        self.comboBoxCaret.addItem("Select Output", "selectOutput")
        self.comboBoxCaret.addItem("Interpolate by Char", "interpolateByChar")
        self.comboBoxCaret.addItem("Interpolate by Line", "interpolateByLine")
        self.comboBoxCaret.addItem("Heuristic", "heuristic")
        self.comboBoxCaret.currentIndexChanged[int].connect(self.on_comboBoxCaret_changed)
        
        self.labelInputOption.setVisible(False)
        self.comboBoxFallbackInput.setVisible(False)
        
        self.command.setTabStopWidth(TABWIDTH)
        
        self.menuCommandTemplates = QtGui.QMenu()
        
        #for name, templateText in self.COMMAND_TEMPLATES.items():
        #    action = self.menuCommandTemplates.addAction(name)
        #    receiver = lambda template = templateText: self.command.setPlainText(template)
        #    self.connect(action, QtCore.SIGNAL('triggered()'), receiver)
        # TODO Este menu ponerlo como menu contextual    
        # self.pushButtonOptions.setMenu(self.menuCommandTemplates)

    @QtCore.Slot()
    def on_command_textChanged(self):
        self.changes['command'] = self.command.toPlainText()
        
    def on_comboBoxBeforeRunning_changed(self, index):
        self.changes['beforeRunningCommand'] = self.comboBoxBeforeRunning.itemData(index)
            
    def on_comboBoxInput_changed(self, index):
        value = self.comboBoxInput.itemData(index)
        self.changes['input'] = value
        if value == 'selection':
            self.labelInputOption.setVisible(True)
            self.comboBoxFallbackInput.setVisible(True)
            index = self.comboBoxFallbackInput.findData(self.changes["fallbackInput"] or "document")
            if index != -1:
                self.comboBoxFallbackInput.setCurrentIndex(index)
        else:
            self.changes.pop('fallbackInput', None)
            self.labelInputOption.setVisible(False)
            self.comboBoxFallbackInput.setVisible(False)
    
    def on_comboBoxFallbackInput_changed(self, index):
        self.changes['fallbackInput'] = self.comboBoxFallbackInput.itemData(index)

    def on_comboBoxInputFormat_changed(self, index):
        self.changes['inputFormat'] = self.comboBoxInputFormat.itemData(index)

    def on_comboBoxOutput_changed(self, index):
        value = self.comboBoxOutput.itemData(index)
        outputKey = "outputLocation" if self.changes["version"] == 2 else "output"
        self.changes[outputKey] = value
    
    def on_comboBoxOutputFormat_changed(self, index):
        self.changes['outputFormat'] = self.comboBoxOutputFormat.itemData(index)
    
    def on_comboBoxCaret_changed(self, index):
        self.changes['outputCaret'] = self.comboBoxCaret.itemData(index)
    
    def getScope(self):
        return super(CommandEditorWidget, self).getScope() or ""
        
    def getTabTrigger(self):
        return  super(CommandEditorWidget, self).getTabTrigger() or ""
    
    def getKeyEquivalent(self):
        return super(CommandEditorWidget, self).getKeyEquivalent() or ""
    
    def getSemanticClass(self):
        return super(CommandEditorWidget, self).getSemanticClass() or ""
    
    def edit(self, bundleItem):
        super(CommandEditorWidget, self).edit(bundleItem)
        #Command
        self.command.setPlainText(self.changes["command"])
        
        #BeforeRunningCommand
        index = self.comboBoxBeforeRunning.findData(self.changes["beforeRunningCommand"])
        if index != -1:
            self.comboBoxBeforeRunning.setCurrentIndex(index)

        #Input
        index = self.comboBoxInput.findData(self.changes["input"])
        if index != -1:
            self.comboBoxInput.setCurrentIndex(index)
    
        #Output
        index = self.comboBoxOutput.findData(self.changes["output"])
        if index != -1:
            self.comboBoxOutput.setCurrentIndex(index)
    
        if self.changes["version"] == 2:
            #Input Format
            index = self.comboBoxInputFormat.findData(self.changes["inputFormat"])
            if index != -1:
                self.comboBoxInputFormat.setCurrentIndex(index)
            
            #Output Format
            index = self.comboBoxOutputFormat.findData(self.changes["outputFormat"])
            if index != -1:
                self.comboBoxOutputFormat.setCurrentIndex(index)
            
            #Output Format
            index = self.comboBoxCaret.findData(self.changes["outputCaret"])
            if index != -1:
                self.comboBoxCaret.setCurrentIndex(index)
            
class TemplateEditorWidget(BundleItemEditorBaseWidget, Ui_Template):
    TYPE = 'template'
    DEFAULTS = {'extension': 'txt',
                'command': '''if [[ ! -f "$TM_NEW_FILE" ]]; then
  TM_YEAR=`date +%Y` \
  TM_DATE=`date +%Y-%m-%d` \
  perl -pe 's/\$\{([^}]*)\}/$ENV{$1}/g' \
     < template_in.txt > "$TM_NEW_FILE"
fi"'''}
    def __init__(self, parent = None):
        BundleItemEditorBaseWidget.__init__(self, parent)
        self.setupUi(self)
        self.comboBoxOutput.addItem("Insert as Text", "insertText")
        self.command.setTabStopWidth(TABWIDTH)

    @QtCore.Slot()
    def on_command_textChanged(self):
        text = self.command.toPlainText()
        if self.bundleItem.command != text:
            self.changes['command'] = text
        else:
            self.changes.pop('command', None)
    
    @QtCore.Slot(str)
    def on_lineEditExtension_textEdited(self, text):
        if text != self.bundleItem.extension:
            self.changes['extension'] = text
        else:
            self.changes.pop('extension', None)
    
    def edit(self, bundleItem):
        super(TemplateEditorWidget, self).edit(bundleItem)
        command = bundleItem.command
        if command is None:
            command = self.DEFAULTS['command']
        self.command.setPlainText(command)
        extension = bundleItem.extension
        if extension is None:
            extension = self.changes['extension'] = self.DEFAULTS['extension']
        self.lineEditExtension.setText(extension)

#TODO: Ui_TemplateFile --> Ui_StaticFile
class StaticFileEditorWidget(BundleItemEditorBaseWidget, Ui_TemplateFile):
    TYPE = 'staticfile'
    DEFAULTS = {'content': '''//
//  ${TM_NEW_FILE_BASENAME}
//
//  Created by ${TM_FULLNAME} on ${TM_DATE}.
//  Copyright (c) ${TM_YEAR} ${TM_ORGANIZATION_NAME}. All rights reserved.
//'''}
    def __init__(self, parent = None):
        BundleItemEditorBaseWidget.__init__(self, parent)
        self.setupUi(self)
        self.content.setTabStopWidth(TABWIDTH)

    @QtCore.Slot()
    def on_content_textChanged(self):
        text = self.content.toPlainText()
        if self.bundleItem.content != text:
            self.changes['content'] = text
        else:
            self.changes.pop('content', None)
    
    def getScope(self):
        return None
    
    def getTabTrigger(self):
        return None
    
    def getKeyEquivalent(self):
        return None
    
    def getSemanticClass(self):
        return None
    
    def edit(self, bundleItem):
        super(StaticFileEditorWidget, self).edit(bundleItem)
        content = bundleItem.content
        if content is None:
            content = self.DEFAULTS['content']
        self.content.setPlainText(content)
    
class DragCommandEditorWidget(BundleItemEditorBaseWidget, Ui_DragCommand):
    TYPE = 'dragcommand'
    def __init__(self, parent = None):
        BundleItemEditorBaseWidget.__init__(self, parent)
        self.setupUi(self)
        self.comboBoxOutput.addItem("Insert as Snippet", "insertAsSnippet")
        self.command.setTabStopWidth(TABWIDTH)
    
    @QtCore.Slot()
    def on_command_textChanged(self):
        self.changes['command'] = self.command.toPlainText()
    
    @QtCore.Slot(str)
    def on_lineEditExtensions_textEdited(self, text):
        value = [item.strip() for item in text.split(",")]
        self.changes['draggedFileExtensions'] = value
        
    def getScope(self):
        return super(DragCommandEditorWidget, self).getScope() or ""
        
    def edit(self, bundleItem):
        BundleItemEditorBaseWidget.edit(self, bundleItem)
        self.command.setPlainText(self.changes['command'])
        self.lineEditExtensions.setText(", ".join(self.changes['draggedFileExtensions']))

class LanguageEditorWidget(BundleItemEditorBaseWidget, Ui_Language):
    TYPE = 'syntax'
    def __init__(self, parent = None):
        BundleItemEditorBaseWidget.__init__(self, parent)
        self.setupUi(self)
        self.content.setTabStopWidth(TABWIDTH)

    def isChanged(self):
        return False

    @QtCore.Slot()
    def on_content_textChanged(self):
        #Convertir a dict
        try:
            grammar = self.command.toPlainText()
            self.changes['grammar'] = ast.literal_eval(grammar)
        except:
            pass
    
    def getKeyEquivalent(self):
        return super(LanguageEditorWidget, self).getKeyEquivalent() or ""
    
    def edit(self, bundleItem):
        BundleItemEditorBaseWidget.edit(self, bundleItem)
        self.changes = {
            "name" : self.changes.pop("name"),
            "uuid" :self.changes.pop("uuid"),
            "grammar": self.changes
        }
        self.content.setPlainText(pformat(self.changes["grammar"]))
    
class PreferenceEditorWidget(BundleItemEditorBaseWidget, Ui_Preference):
    TYPE = 'preference'
    def __init__(self, parent = None):
        BundleItemEditorBaseWidget.__init__(self, parent)
        self.setupUi(self)
        self.settings.setTabStopWidth(TABWIDTH)
    
    @QtCore.Slot()
    def on_settings_textChanged(self):
        #Convertir a dict
        try:
            settings = self.settings.toPlainText()
            self.changes['settings'] = ast.literal_eval(settings)
        except:
            # Un mensaje de error estaria bueno no? :)
            pass

    def getScope(self):
        return super(PreferenceEditorWidget, self).getScope() or ""
    
    def edit(self, bundleItem):
        BundleItemEditorBaseWidget.edit(self, bundleItem)
        self.settings.setPlainText(pformat(self.changes['settings']))

class MacroEditorWidget(BundleItemEditorBaseWidget, Ui_Macro):
    TYPE = 'macro'
    COMMAND = 0
    def __init__(self, parent = None):
        BundleItemEditorBaseWidget.__init__(self, parent)
        self.setupUi(self)
        self.argument.setTabStopWidth(TABWIDTH)
    
    def on_listActionWidget_itemClicked(self, item):
        index = self.listActionWidget.indexFromItem(item)
        row = index.row()
        if 'argument' in self.changes["commands"][row]:
            self.argument.setPlainText(pformat(self.changes["commands"][row]['argument']))
        else:
            self.argument.clear()

    def edit(self, bundleItem):
        BundleItemEditorBaseWidget.edit(self, bundleItem)
        self.listActionWidget.clear()
        self.argument.clear()
        for command in self.changes["commands"]:
            item = QtGui.QListWidgetItem(command['command'], self.listActionWidget, self.COMMAND)
            self.listActionWidget.addItem(item)

class BundleEditorWidget(BundleItemEditorBaseWidget, Ui_Menu):
    TYPE = 'bundle'
    def __init__(self, parent = None):
        super(BundleEditorWidget, self).__init__(parent)
        self.setupUi(self)
        manager = parent.manager

        self.treeMenuModel = BundleItemMenuTreeModel(manager)
        self.treeMenuView.setModel(self.treeMenuModel)
        self.listExcludedView.setModel(self.treeMenuModel.excludedListModel())

        self.treeMenuModel.menuChanged.connect(self.on_menuChanged)

    def on_menuChanged(self):
        self.changes['mainMenu'] = self.treeMenuModel.getMainMenu()

    def getScope(self):
        return None
    
    def getTabTrigger(self):
        return None
    
    def getKeyEquivalent(self):
        return None
    
    def getSemanticClass(self):
        return None
    
    def edit(self, bundleItem):
        BundleItemEditorBaseWidget.edit(self, bundleItem)
        self.treeMenuModel.setBundle(bundleItem)

class ProjectEditorWidget(BundleItemEditorBaseWidget, Ui_Project):
    TYPE = 'project'

    def __init__(self, parent = None):
        BundleItemEditorBaseWidget.__init__(self, parent)
        self.setupUi(self)
        self.command.setTabStopWidth(TABWIDTH)

    @QtCore.Slot()
    def on_command_textChanged(self):
        self.changes['command'] = self.command.toPlainText()
    
    def edit(self, bundleItem):
        BundleItemEditorBaseWidget.edit(self, bundleItem)
        self.command.setPlainText(self.cahnges['command'])
