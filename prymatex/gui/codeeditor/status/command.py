#!/usr/bin/env python
from __future__ import unicode_literals

class CommandMixin(object):
    """docstring for FindMixin"""
    def __init__(self, **kwargs):
        super(CommandMixin, self).__init__(**kwargs)

    def initialize(self, *args, **kwargs):
        self.widgetCommand.setVisible(False)

    def setup(self):
        self.comboBoxInput.addItem("None", "none")
        self.comboBoxInput.addItem("Selected Text", "selection")
        self.comboBoxInput.addItem("Entire Document", "document")
        
        self.comboBoxOutput.addItem("Discard", "discard")
        self.comboBoxOutput.addItem("Replace Selected Text", "replaceSelectedText")
        self.comboBoxOutput.addItem("Replace Document", "replaceDocument")
        self.comboBoxOutput.addItem("Insert as Text", "insertText")
        self.comboBoxOutput.addItem("Insert as Snippet", "insertAsSnippet")
        self.comboBoxOutput.addItem("Show as HTML", "showAsHTML")
        self.comboBoxOutput.addItem("Show as Tool Tip", "showAsTooltip")
        self.comboBoxOutput.addItem("Create New Document", "createNewDocument")
        self.comboBoxOutput.setCurrentIndex(3)
        self.comboBoxCommand.lineEdit().returnPressed.connect(self.on_comboBoxCommand_returnPressed)
    
    def filterThroughCommand(self):
        self.hideAll()
        self.widgetCommand.setVisible(True)
        
    # ------- Signals
    def on_comboBoxCommand_returnPressed(self):
        editor = self.window().currentEditor() 
        command = self.comboBoxCommand.lineEdit().text()
        _input = self.comboBoxInput.itemData(self.comboBoxInput.currentIndex())
        _output = self.comboBoxOutput.itemData(self.comboBoxOutput.currentIndex())
        editor.insertCommand(command, _input, _output)
        self.comboBoxCommand.lineEdit().clear()