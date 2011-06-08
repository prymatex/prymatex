# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui

from prymatex.gui.bundles.ui_snippet import Ui_Snippet
from prymatex.gui.bundles.ui_command import Ui_Command
from prymatex.gui.bundles.ui_template import Ui_Template
from prymatex.gui.bundles.ui_dragcommand import Ui_DragCommand
from prymatex.gui.bundles.ui_language import Ui_Language
from prymatex.gui.bundles.ui_menu import Ui_Menu
from prymatex.gui.bundles.ui_templatefile import Ui_TemplateFile
from prymatex.gui.bundles.ui_preference import Ui_Preference
from pprint import pformat

class PMXEditorBaseWidget(QtGui.QWidget):
    '''
        Base class for editors  
    '''
    TYPE = ''
    
    def __init__(self, parent = None):
        super(PMXEditorBaseWidget, self).__init__(parent)
        #The bundle item
        self.current = None
    
    def title(self):
        return 'No item selected'
    
    @property
    def scope(self):
        if self.current == None or not hasattr(self.current, 'scope'):
            return None
        return self.current.scope 
        
    @property
    def tabTrigger(self):
        if self.current == None or not hasattr(self.current, 'tabTrigger'):
            return None
        return self.current.tabTrigger
    
    @property
    def keyEquivalent(self):
        if self.current == None or not hasattr(self.current, 'keyEquivalent'):
            return None
        return self.current.keyEquivalent
    
    def edit(self, bundleItem):
        self.current = bundleItem

#============================================================
# Snippet Editor Widget
#============================================================
class PMXSnippetWidget(PMXEditorBaseWidget, Ui_Snippet):
    TYPE = 'snippet'
    def __init__(self, parent = None):
        super(PMXSnippetWidget, self).__init__(parent)
        self.setupUi(self)

    def title(self):
        if self.current != None:
            return 'Edit Snippet: "%s"' % self.current.name
        return super(PMXSnippetWidget, self).title()

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
        self.comboBoxInput.addItem("None", QtCore.QVariant("none"))
        self.comboBoxInput.addItem("Selected Text", QtCore.QVariant("selection")) #selectedText
        self.comboBoxInput.addItem("Entire Document", QtCore.QVariant("document"))
        self.comboBoxFallbackInput.addItem("Document", QtCore.QVariant("document"))
        self.comboBoxFallbackInput.addItem("Line", QtCore.QVariant("line"))
        self.comboBoxFallbackInput.addItem("Word", QtCore.QVariant("word"))
        self.comboBoxFallbackInput.addItem("Character", QtCore.QVariant("character"))
        self.comboBoxFallbackInput.addItem("Scope", QtCore.QVariant("scope"))
        self.comboBoxFallbackInput.addItem("Nothing", QtCore.QVariant("none"))
        self.comboBoxOutput.addItem("Discard", QtCore.QVariant("discard"))
        self.comboBoxOutput.addItem("Replace Selected Text", QtCore.QVariant("replaceSelectedText"))
        self.comboBoxOutput.addItem("Replace Document", QtCore.QVariant("replaceDocument"))
        self.comboBoxOutput.addItem("Insert as Text", QtCore.QVariant("insertText"))
        self.comboBoxOutput.addItem("Insert as Snippet", QtCore.QVariant("insertAsSnippet"))
        self.comboBoxOutput.addItem("Show as HTML", QtCore.QVariant("showAsHTML"))
        self.comboBoxOutput.addItem("Show as Tool Tip", QtCore.QVariant("showAsTooltip"))
        self.comboBoxOutput.addItem("Create New Document", QtCore.QVariant("createNewDocument"))
        
    def title(self):
        if self.current != None:
            return 'Edit Command: "%s"' % self.current.name
        return super(PMXCommandWidget, self).title()
    
    def edit(self, bundleItem):
        super(PMXCommandWidget, self).edit(bundleItem)
        hash = bundleItem.hash
        self.command.setPlainText(hash['command'])
        index = self.comboBoxBeforeRunning.findData(QtCore.QVariant(hash['beforeRunningCommand']))
        if index != -1:
            self.comboBoxBeforeRunning.setCurrentIndex(index)
        index = self.comboBoxInput.findData(QtCore.QVariant(hash['input']))
        if index != -1:
            self.comboBoxInput.setCurrentIndex(index)
        #Opcional solo si input es igual a selectedText
        if hash['input'] == 'selection' and 'fallbackInput' in hash:
            self.labelInputOption.setVisible(True)
            self.comboBoxFallbackInput.setVisible(True)
            index = self.comboBoxFallbackInput.findData(QtCore.QVariant(hash['fallbackInput']))
            if index != -1:
                self.comboBoxFallbackInput.setCurrentIndex(index)
        else:
            self.labelInputOption.setVisible(False)
            self.comboBoxFallbackInput.setVisible(False)
        index = self.comboBoxOutput.findData(QtCore.QVariant(hash['output']))
        if index != -1:
            self.comboBoxOutput.setCurrentIndex(index)
        
    
class PMXTemplateWidget(PMXEditorBaseWidget, Ui_Template):
    TYPE = 'template'
    def __init__(self, parent = None):
        super(PMXTemplateWidget, self).__init__(parent)
        self.setupUi(self)
        self.comboBoxOutput.addItem("Insert as Text", QtCore.QVariant("insertText"))

    def title(self):
        if self.current != None:
            return 'Edit Template: "%s"' % self.current.name
        return super(PMXTemplateWidget, self).title()

    def edit(self, bundleItem):
        super(PMXTemplateWidget, self).edit(bundleItem)
        hash = bundleItem.hash
        self.command.setPlainText(hash['command'])
        self.lineEditExtension.setText(hash['extension'])

class PMXTemplateFileWidget(PMXEditorBaseWidget, Ui_TemplateFile):
    TYPE = 'templatefile'
    def __init__(self, parent = None):
        super(PMXTemplateFileWidget, self).__init__(parent)
        self.setupUi(self) 

    def title(self):
        if self.current != None:
            return 'Edit Template File: "%s"' % self.current.name
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

    def title(self):
        if self.current != None:
            return 'Edit Drag Command: "%s"' % self.current.name
        return super(PMXDragCommandWidget, self).title()

    def edit(self, bundleItem):
        super(PMXDragCommandWidget, self).edit(bundleItem)
        hash = bundleItem.hash
        self.command.setPlainText(hash['command'])
        self.lineEditExtensions.setText(", ".join(hash['draggedFileExtensions']))

class PMXLanguageWidget(PMXEditorBaseWidget, Ui_Language):
    TYPE = 'syntax'
    def __init__(self, parent = None):
        super(PMXLanguageWidget, self).__init__(parent)
        self.setupUi(self)
    
    def title(self):
        if self.current != None:
            return 'Edit Language: "%s"' % self.current.name
        return super(PMXLanguageWidget, self).title()
    
    def edit(self, bundleItem):
        super(PMXLanguageWidget, self).edit(bundleItem)
        hash = bundleItem.hash
        self.content.setPlainText(pformat(hash))
    
class PMXBundleWidget(PMXEditorBaseWidget, Ui_Menu):
    TYPE = 'bundle'
    def __init__(self, parent = None):
        super(PMXBundleWidget, self).__init__(parent)
        self.setupUi(self)

class PMXPreferenceWidget(PMXEditorBaseWidget, Ui_Preference):
    TYPE = 'preference'
    def __init__(self, parent = None):
        super(PMXPreferenceWidget, self).__init__(parent)
        self.setupUi(self)
    
    def title(self):
        if self.current != None:
            return 'Edit Preferences: "%s"' % self.current.name
        return super(PMXPreferenceWidget, self).title()
    
    def edit(self, bundleItem):
        super(PMXPreferenceWidget, self).edit(bundleItem)
        hash = bundleItem.hash
        self.settings.setPlainText(pformat(hash['settings']))