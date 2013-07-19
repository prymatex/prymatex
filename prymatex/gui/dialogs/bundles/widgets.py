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
        self.__title = 'Edit %s: "%s"' % (self.TYPE, bundleItem.name)
        self.changes = bundleItem.dump()

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
    DEFAULTS = {'beforeRunningCommand': 'nop',
                'command': '''# just to remind you of some useful environment variables
# see Help / Environment Variables for the full list
echo File: "$TM_FILEPATH"
echo Word: "$TM_CURRENT_WORD"
echo Selection: "$TM_SELECTED_TEXT"''',
                'input': 'selection',
                'inputFormat': 'text',
                'fallbackInput': 'document',
                'output': 'replaceSelectedText',
                'outputFormat': 'text',
                'outputCaret': 'afterOutput'}
    
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
        text = self.command.toPlainText()
        if self.bundleItem.command != text:
            self.changes['command'] = text
        else:
            self.changes.pop('command', None)
        
    def on_comboBoxBeforeRunning_changed(self, index):
        value = self.comboBoxBeforeRunning.itemData(index)
        if value != self.bundleItem.beforeRunningCommand:
            self.changes['beforeRunningCommand'] = value
        else:
            self.changes.pop('beforeRunningCommand', None)
            
    def on_comboBoxInput_changed(self, index):
        value = self.comboBoxInput.itemData(index)
        if value != self.bundleItem.input:
            self.changes['input'] = value
        else:
            self.changes.pop('input', None)
        if value == 'selection':
            self.labelInputOption.setVisible(True)
            self.comboBoxFallbackInput.setVisible(True)
            fallbackInput = self.bundleItem.fallbackInput
            if fallbackInput is None:
                fallbackInput = self.DEFAULTS['fallbackInput']
            index = self.comboBoxFallbackInput.findData(fallbackInput)
            if index != -1:
                self.comboBoxFallbackInput.setCurrentIndex(index)
        else:
            self.changes.pop('fallbackInput', None)
            self.labelInputOption.setVisible(False)
            self.comboBoxFallbackInput.setVisible(False)
    
    def on_comboBoxFallbackInput_changed(self, index):
        value = self.comboBoxFallbackInput.itemData(index)
        if value != self.bundleItem.fallbackInput and value != self.DEFAULTS['fallbackInput']:
            self.changes['fallbackInput'] = value
        else:
            self.changes.pop('fallbackInput', None)
    
    def on_comboBoxInputFormat_changed(self, index):
        value = self.comboBoxInputFormat.itemData(index)
        if value != self.bundleItem.inputFormat:
            self.changes['inputFormat'] = value
        else:
            self.changes.pop('inputFormat', None)

    def on_comboBoxOutput_changed(self, index):
        value = self.comboBoxOutput.itemData(index)
        outputKey = "outputLocation" if self.bundleItem.version == 2 else "output"
        if value != getattr(self.bundleItem, outputKey):
            self.changes[outputKey] = value
        else:
            self.changes.pop(outputKey, None)
    
    def on_comboBoxOutputFormat_changed(self, index):
        value = self.comboBoxOutputFormat.itemData(index)
        if value != self.bundleItem.outputFormat:
            self.changes['outputFormat'] = value
        else:
            self.changes.pop('outputFormat', None)
    
    def on_comboBoxCaret_changed(self, index):
        value = self.comboBoxCaret.itemData(index)
        if value != self.bundleItem.outputCaret:
            self.changes['outputCaret'] = value
        else:
            self.changes.pop('outputCaret', None)
    
    def getScope(self):
        scope = super(CommandEditorWidget, self).getScope()
        return scope is not None and scope or ""
        
    def getTabTrigger(self):
        tabTrigger = super(CommandEditorWidget, self).getTabTrigger()
        return  tabTrigger is not None and tabTrigger or ""
    
    def getKeyEquivalent(self):
        keyEquivalent = super(CommandEditorWidget, self).getKeyEquivalent()
        return keyEquivalent is not None and keyEquivalent or ""
    
    def getSemanticClass(self):
        semanticClass = super(CommandEditorWidget, self).getSemanticClass()
        return semanticClass is not None and semanticClass or ""
    
    def edit(self, bundleItem):
        super(CommandEditorWidget, self).edit(bundleItem)
        #Command
        command = bundleItem.command
        if command is None:
            command = self.DEFAULTS['command']
        self.command.setPlainText(command)
        
        #BeforeRunningCommand
        beforeRunningCommand = bundleItem.beforeRunningCommand
        if beforeRunningCommand is None:
            beforeRunningCommand = self.changes['beforeRunningCommand'] = self.DEFAULTS['beforeRunningCommand']
        index = self.comboBoxBeforeRunning.findData(beforeRunningCommand)
        if index != -1:
            self.comboBoxBeforeRunning.setCurrentIndex(index)

        #Input
        commandInput = bundleItem.input
        if commandInput is None:
            commandInput = self.changes['input'] = self.DEFAULTS['input']
        index = self.comboBoxInput.findData(commandInput)
        if index != -1:
            self.comboBoxInput.setCurrentIndex(index)
    
        #Output
        output = bundleItem.output or bundleItem.outputLocation
        if output is None:
            output = self.changes['output'] = self.DEFAULTS['output']
        index = self.comboBoxOutput.findData(output)
        if index != -1:
            self.comboBoxOutput.setCurrentIndex(index)
    
        if bundleItem.version == 2:
            #Input Format
            commandInputFormat = bundleItem.inputFormat
            if commandInputFormat is None:
                commandInputFormat = self.changes['inputFormat'] = self.DEFAULTS['inputFormat']
            index = self.comboBoxInputFormat.findData(commandInputFormat)
            if index != -1:
                self.comboBoxInputFormat.setCurrentIndex(index)
            
            #Output Format
            commandOutputFormat = bundleItem.outputFormat
            if commandOutputFormat is None:
                commandOutputFormat = self.changes['outputFormat'] = self.DEFAULTS['outputFormat']
            index = self.comboBoxOutputFormat.findData(commandOutputFormat)
            if index != -1:
                self.comboBoxOutputFormat.setCurrentIndex(index)
            
            #Output Format
            commandOutputCaret = bundleItem.outputCaret
            if commandOutputCaret is None:
                commandOutputCaret = self.changes['outputCaret'] = self.DEFAULTS['outputCaret']
            index = self.comboBoxCaret.findData(commandOutputCaret)
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
    DEFAULTS = {'draggedFileExtensions': ['png', 'jpg'],
                'command': '''echo "$TM_DROPPED_FILE"'''}
    def __init__(self, parent = None):
        BundleItemEditorBaseWidget.__init__(self, parent)
        self.setupUi(self)
        self.comboBoxOutput.addItem("Insert as Snippet", "insertAsSnippet")
        self.command.setTabStopWidth(TABWIDTH)
    
    @QtCore.Slot()
    def on_command_textChanged(self):
        text = self.command.toPlainText()
        if self.bundleItem.command != text:
            self.changes['command'] = text
        else:
            self.changes.pop('command', None)
    
    @QtCore.Slot(str)
    def on_lineEditExtensions_textEdited(self, text):
        value = [item.strip() for item in text.split(",")]
        if value != self.bundleItem.draggedFileExtensions:
            self.changes['draggedFileExtensions'] = value
        else:
            self.changes.pop('draggedFileExtensions', None)
        
    def getScope(self):
        scope = super(DragCommandEditorWidget, self).getScope()
        return scope is not None and scope or ""
        
    def edit(self, bundleItem):
        super(DragCommandEditorWidget, self).edit(bundleItem)
        command = bundleItem.command
        if command is None:
            command = self.DEFAULTS['command']
        self.command.setPlainText(command)
        draggedFileExtensions = bundleItem.draggedFileExtensions
        if draggedFileExtensions is None:
            draggedFileExtensions = self.changes['draggedFileExtensions'] = self.DEFAULTS['draggedFileExtensions']
        self.lineEditExtensions.setText(", ".join(draggedFileExtensions))

class LanguageEditorWidget(BundleItemEditorBaseWidget, Ui_Language):
    TYPE = 'syntax'
    DEFAULTS = {'content': {       'scopeName': 'source.untitled',
       'fileTypes': [],
       'foldingStartMarker': '/\*\*|\{\s*$',
       'foldingStopMarker': '\*\*/|^\s*\}',
       'patterns': [
               {       'name': 'keyword.control.untitled',
                       'match': '\b(if|while|for|return)\b' },
               {       'name': 'string.quoted.double.untitled',
                       'begin': '"',
                       'end': '"',
                       'patterns': [
                               {     'name': 'constant.character.escape.untitled',
                                     'match': '\\.' } ]
               }
       ]}
    }
    def __init__(self, parent = None):
        BundleItemEditorBaseWidget.__init__(self, parent)
        self.setupUi(self)
        self.content.setTabStopWidth(TABWIDTH)
    
    @QtCore.Slot()
    def on_content_textChanged(self):
        #Convertir a dict
        try:
            self.changes['content'] = ast.literal_eval(self.command.toPlainText())
        except:
            pass
    
    def getKeyEquivalent(self):
        keyEquivalent = super(LanguageEditorWidget, self).getKeyEquivalent()
        return keyEquivalent is not None and keyEquivalent or ""
    
    def edit(self, bundleItem):
        super(LanguageEditorWidget, self).edit(bundleItem)
        content = bundleItem.dump()
        content.pop('name')
        content.pop('uuid')
        if len(content) == 0:
            content = self.changes['content'] = self.DEFAULTS['content']
        self.content.setPlainText(pformat(content))
    
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
            settings = ast.literal_eval(self.settings.toPlainText())
            if self.bundleItem.dump()["settings"] != settings:
                self.changes['settings'] = settings
            else:
                self.changes.pop("settings", None)
        except:
            pass

    def getScope(self):
        scope = super(PreferenceEditorWidget, self).getScope()
        return scope is not None and scope or ""
    
    def edit(self, bundleItem):
        super(PreferenceEditorWidget, self).edit(bundleItem)
        content = bundleItem.dump()
        self.settings.setPlainText(pformat(content['settings']))

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
        if 'argument' in self.bundleItem.commands[row]:
            self.argument.setPlainText(pformat(self.bundleItem.commands[row]['argument']))
        else:
            self.argument.clear()

    def edit(self, bundleItem):
        BundleItemEditorBaseWidget.edit(self, bundleItem)
        self.listActionWidget.clear()
        self.argument.clear()
        commands = bundleItem.commands
        for command in commands:
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
    
    def edit(self, bundle):
        super(BundleEditorWidget, self).edit(bundle)
        self.treeMenuModel.setBundle(bundle)

class ProjectEditorWidget(BundleItemEditorBaseWidget, Ui_Project):
    TYPE = 'project'
    DEFAULTS = {
                'command': '''if [[ ! -f "$TM_NEW_PROJECT_LOCATION" ]]; then
  TM_YEAR=`date +%Y` \
  TM_DATE=`date +%Y-%m-%d` \
  perl -pe 's/\$\{([^}]*)\}/$ENV{$1}/g' \
     < template_in.txt > "$TM_NEW_PROJECT_LOCATION"
fi"'''}
    def __init__(self, parent = None):
        BundleItemEditorBaseWidget.__init__(self, parent)
        self.setupUi(self)
        self.command.setTabStopWidth(TABWIDTH)

    @QtCore.Slot()
    def on_command_textChanged(self):
        self.changes['command'] = self.command.toPlainText()
    
    def edit(self, bundleItem):
        super(ProjectEditorWidget, self).edit(bundleItem)
        command = bundleItem.command
        if command is None:
            command = self.DEFAULTS['command']
        self.command.setPlainText(command)
