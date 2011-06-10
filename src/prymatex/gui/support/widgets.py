#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui

from prymatex.gui.support.ui_snippet import Ui_Snippet
from prymatex.gui.support.ui_command import Ui_Command
from prymatex.gui.support.ui_template import Ui_Template
from prymatex.gui.support.ui_dragcommand import Ui_DragCommand
from prymatex.gui.support.ui_language import Ui_Language
from prymatex.gui.support.ui_menu import Ui_Menu
from prymatex.gui.support.ui_templatefile import Ui_TemplateFile
from prymatex.gui.support.ui_preference import Ui_Preference
from pprint import pformat

class PMXEditorBaseWidget(QtGui.QWidget):
    '''
        Base class for editors  
    '''
    TYPE = ''
    
    def __init__(self, parent = None):
        super(PMXEditorBaseWidget, self).__init__(parent)
        #The bundle item
        self.bundleItem = None
        self.changes = {}
    
    @property
    def isChanged(self):
        return bool(self.changes)
    
    @property
    def title(self):
        return 'No item selected'
    
    def getScope(self):
        if self.bundleItem is None:
            return None
        return self.bundleItem.scope
    
    def setScope(self, value):
        current = self.getScope()
        if value is not None and current is not None:
            if value != current:
                self.changes['scope'] = value
            else:
                self.changes.pop('scope', None)
        elif value is None and current is not None:
            self.changes['scope'] = value
        else:
            self.changes.pop('scope', None)

    def getTabTrigger(self):
        if self.bundleItem is None:
            return None
        return self.bundleItem.tabTrigger
    
    def setTabTrigger(self, value):
        current = self.getTabTrigger()
        if value is not None and current is not None:
            if value != current:
                self.changes['tabTrigger'] = value
            else:
                self.changes.pop('tabTrigger', None)
        elif value is None and current is not None:
            self.changes['tabTrigger'] = value
        else:
            self.changes.pop('tabTrigger', None)
    
    def getKeyEquivalent(self):
        if self.bundleItem is None:
            return None
        return self.bundleItem.keyEquivalent
    
    def setKeyEquivalent(self, value):
        current = self.getKeyEquivalent()
        if value is not None and current is not None:
            if value != current:
                self.changes['keyEquivalent'] = value
            else:
                self.changes.pop('keyEquivalent', None)
        elif value is None and current is not None:
            self.changes['keyEquivalent'] = value
        else:
            self.changes.pop('keyEquivalent', None)
    
    def edit(self, bundleItem):
        self.changes = {}
        self.bundleItem = bundleItem

#============================================================
# Snippet Editor Widget
#============================================================
class PMXSnippetWidget(PMXEditorBaseWidget, Ui_Snippet):
    TYPE = 'snippet'
    def __init__(self, parent = None):
        super(PMXSnippetWidget, self).__init__(parent)
        self.setupUi(self)

    @property
    def title(self):
        if self.bundleItem != None:
            return 'Edit Snippet: "%s"' % self.bundleItem.name
        return super(PMXSnippetWidget, self).title()

    def getScope(self):
        scope = super(PMXSnippetWidget, self).getScope()
        return scope is not None and scope or ""
    
    def getTabTrigger(self):
        tabTrigger = super(PMXSnippetWidget, self).getTabTrigger()
        return tabTrigger is not None and tabTrigger or ""
    
    def getKeyEquivalent(self):
        keyEquivalent = super(PMXSnippetWidget, self).getKeyEquivalent()
        return keyEquivalent is not None and keyEquivalent or ""
    
    def edit(self, bundleItem):
        super(PMXSnippetWidget, self).edit(bundleItem)
        hash = bundleItem.hash
        self.content.setPlainText(hash['content'])

class PMXCommandWidget(PMXEditorBaseWidget, Ui_Command):
    TYPE = 'command'
    def __init__(self, parent = None):
        super(PMXCommandWidget, self).__init__(parent)
        self.setupUi(self)
        self.comboBoxBeforeRunning.addItem("Nothing", QtCore.QVariant("nop"))
        self.comboBoxBeforeRunning.addItem("Current File", QtCore.QVariant("saveActiveFile"))
        self.comboBoxBeforeRunning.addItem("All Files in Project", QtCore.QVariant("saveModifiedFiles"))
        self.comboBoxBeforeRunning.currentIndexChanged[int].connect(self.on_comboBoxBeforeRunning_changed)
        
        self.comboBoxInput.addItem("None", QtCore.QVariant("none"))
        self.comboBoxInput.addItem("Selected Text", QtCore.QVariant("selection")) #selectedText
        self.comboBoxInput.addItem("Entire Document", QtCore.QVariant("document"))
        self.comboBoxInput.currentIndexChanged[int].connect(self.on_comboBoxInput_changed)
        
        self.comboBoxFallbackInput.addItem("Document", QtCore.QVariant("document"))
        self.comboBoxFallbackInput.addItem("Line", QtCore.QVariant("line"))
        self.comboBoxFallbackInput.addItem("Word", QtCore.QVariant("word"))
        self.comboBoxFallbackInput.addItem("Character", QtCore.QVariant("character"))
        self.comboBoxFallbackInput.addItem("Scope", QtCore.QVariant("scope"))
        self.comboBoxFallbackInput.addItem("Nothing", QtCore.QVariant("none"))
        self.comboBoxFallbackInput.currentIndexChanged[int].connect(self.on_comboBoxFallbackInput_changed)
        
        self.comboBoxOutput.addItem("Discard", QtCore.QVariant("discard"))
        self.comboBoxOutput.addItem("Replace Selected Text", QtCore.QVariant("replaceSelectedText"))
        self.comboBoxOutput.addItem("Replace Document", QtCore.QVariant("replaceDocument"))
        self.comboBoxOutput.addItem("Insert as Text", QtCore.QVariant("insertText"))
        self.comboBoxOutput.addItem("Insert as Snippet", QtCore.QVariant("insertAsSnippet"))
        self.comboBoxOutput.addItem("Show as HTML", QtCore.QVariant("showAsHTML"))
        self.comboBoxOutput.addItem("Show as Tool Tip", QtCore.QVariant("showAsTooltip"))
        self.comboBoxOutput.addItem("Create New Document", QtCore.QVariant("createNewDocument"))
        self.comboBoxOutput.currentIndexChanged[int].connect(self.on_comboBoxOutput_changed)

    def on_comboBoxBeforeRunning_changed(self, index):
        value = self.comboBoxBeforeRunning.itemData(index).toString()
        if value != self.bundleItem.beforeRunningCommand:
            self.changes['beforeRunningCommand'] = unicode(value)
        else:
            self.changes.pop('beforeRunningCommand', None)
            
    def on_comboBoxInput_changed(self, index):
        value = self.comboBoxInput.itemData(index).toString()
        if value != self.bundleItem.input:
            self.changes['input'] = unicode(value)
        else:
            self.changes.pop('input', None)
        if value == 'selection' and self.bundleItem.fallbackInput != None:
            self.labelInputOption.setVisible(True)
            self.comboBoxFallbackInput.setVisible(True)
            index = self.comboBoxFallbackInput.findData(QtCore.QVariant(self.bundleItem.fallbackInput))
            if index != -1:
                self.comboBoxFallbackInput.setCurrentIndex(index)
        else:
            self.labelInputOption.setVisible(False)
            self.comboBoxFallbackInput.setVisible(False)
        
    def on_comboBoxFallbackInput_changed(self, index):
        value = self.comboBoxFallbackInput.itemData(index).toString()
        if value != self.bundleItem.fallbackInput:
            self.changes['fallbackInput'] = unicode(value)
        else:
            self.changes.pop('fallbackInput', None)
        
    def on_comboBoxOutput_changed(self, index):
        value = self.comboBoxOutput.itemData(index).toString()
        if value != self.bundleItem.output:
            self.changes['output'] = unicode(value)
        else:
            self.changes.pop('output', None)
    
    @property
    def title(self):
        if self.bundleItem != None:
            return 'Edit Command: "%s"' % self.bundleItem.name
        return super(PMXCommandWidget, self).title()
    
    def getScope(self):
        scope = super(PMXCommandWidget, self).getScope()
        return scope is not None and scope or ""
        
    def getTabTrigger(self):
        tabTrigger = super(PMXCommandWidget, self).getTabTrigger()
        return  tabTrigger is not None and tabTrigger or ""
    
    def getKeyEquivalent(self):
        keyEquivalent = super(PMXCommandWidget, self).getKeyEquivalent()
        return keyEquivalent is not None and keyEquivalent or ""
    
    def edit(self, bundleItem):
        super(PMXCommandWidget, self).edit(bundleItem)
        self.command.setPlainText(bundleItem.command)
        index = self.comboBoxBeforeRunning.findData(QtCore.QVariant(bundleItem.beforeRunningCommand))
        if index != -1:
            self.comboBoxBeforeRunning.setCurrentIndex(index)
        index = self.comboBoxInput.findData(QtCore.QVariant(bundleItem.input))
        if index != -1:
            self.comboBoxInput.setCurrentIndex(index)
        index = self.comboBoxOutput.findData(QtCore.QVariant(bundleItem.output))
        if index != -1:
            self.comboBoxOutput.setCurrentIndex(index)
    
class PMXTemplateWidget(PMXEditorBaseWidget, Ui_Template):
    TYPE = 'template'
    def __init__(self, parent = None):
        super(PMXTemplateWidget, self).__init__(parent)
        self.setupUi(self)
        self.comboBoxOutput.addItem("Insert as Text", QtCore.QVariant("insertText"))
        self.lineEditExtension.textEdited.connect(self.on_lineEditExtension_edited)
    
    def on_lineEditExtension_edited(self, text):
        value = unicode(text)
        if value != self.bundleItem.extension:
            self.changes['extension'] = value
        else:
            self.changes.pop('extension', None)
            
    @property
    def title(self):
        if self.bundleItem != None:
            return 'Edit Template: "%s"' % self.bundleItem.name
        return super(PMXTemplateWidget, self).title()

    def edit(self, bundleItem):
        super(PMXTemplateWidget, self).edit(bundleItem)
        self.command.setPlainText(bundleItem.command)
        self.lineEditExtension.setText(bundleItem.extension)

class PMXTemplateFileWidget(PMXEditorBaseWidget, Ui_TemplateFile):
    TYPE = 'templatefile'
    def __init__(self, parent = None):
        super(PMXTemplateFileWidget, self).__init__(parent)
        self.setupUi(self)

    @property
    def title(self):
        if self.bundleItem != None:
            return 'Edit Template File: "%s"' % self.bundleItem.name
        return super(PMXTemplateFileWidget, self).title()

    def edit(self, bundleItem):
        super(PMXTemplateFileWidget, self).edit(bundleItem)
        self.content.setPlainText(bundleItem.content)
    
class PMXDragCommandWidget(PMXEditorBaseWidget, Ui_DragCommand):
    TYPE = 'dragcommand'
    def __init__(self, parent = None):
        super(PMXDragCommandWidget, self).__init__(parent)
        self.setupUi(self)
        self.comboBoxOutput.addItem("Insert as Snippet", QtCore.QVariant("insertAsSnippet"))
        self.lineEditExtensions.textEdited.connect(self.on_lineEditExtensions_edited)
    
    def on_lineEditExtensions_edited(self, text):
        value = map(lambda item: item.strip(), unicode(text).split(","))
        if value != self.bundleItem.draggedFileExtensions:
            self.changes['draggedFileExtensions'] = value
        else:
            self.changes.pop('draggedFileExtensions', None)
            
    @property
    def title(self):
        if self.bundleItem != None:
            return 'Edit Drag Command: "%s"' % self.bundleItem.name
        return super(PMXDragCommandWidget, self).title()
        
    def getScope(self):
        scope = super(PMXDragCommandWidget, self).getScope()
        return scope is not None and scope or ""
        
    def edit(self, bundleItem):
        super(PMXDragCommandWidget, self).edit(bundleItem)
        self.command.setPlainText(bundleItem.command)
        self.lineEditExtensions.setText(", ".join(bundleItem.draggedFileExtensions))

class PMXLanguageWidget(PMXEditorBaseWidget, Ui_Language):
    TYPE = 'syntax'
    def __init__(self, parent = None):
        super(PMXLanguageWidget, self).__init__(parent)
        self.setupUi(self)
    
    @property
    def title(self):
        if self.bundleItem != None:
            return 'Edit Language: "%s"' % self.bundleItem.name
        return super(PMXLanguageWidget, self).title()
    
    def getScope(self):
        scope = super(PMXLanguageWidget, self).getScope()
        return scope is not None and scope or ""
    
    def edit(self, bundleItem):
        super(PMXLanguageWidget, self).edit(bundleItem)
        hash = bundleItem.hash
        self.content.setPlainText(pformat(hash))
    
class PMXPreferenceWidget(PMXEditorBaseWidget, Ui_Preference):
    TYPE = 'preference'
    def __init__(self, parent = None):
        super(PMXPreferenceWidget, self).__init__(parent)
        self.setupUi(self)
    
    @property
    def title(self):
        if self.bundleItem != None:
            return 'Edit Preferences: "%s"' % self.bundleItem.name
        return super(PMXPreferenceWidget, self).title()
    
    def getScope(self):
        scope = super(PMXPreferenceWidget, self).getScope()
        return scope is not None and scope or ""
    
    def edit(self, bundleItem):
        super(PMXPreferenceWidget, self).edit(bundleItem)
        hash = bundleItem.hash
        self.settings.setPlainText(pformat(hash['settings']))

class PMXBundleWidget(PMXEditorBaseWidget, Ui_Menu):
    TYPE = 'bundle'
    def __init__(self, parent = None):
        super(PMXBundleWidget, self).__init__(parent)
        self.setupUi(self)
    
    @property
    def title(self):
        if self.bundleItem != None:
            return 'Edit Menu: "%s"' % self.bundleItem.name
        return super(PMXBundleWidget, self).title()
        
    def getScope(self):
        return None
    
    def getTabTrigger(self):
        return None
    
    def getKeyEquivalent(self):
        return None