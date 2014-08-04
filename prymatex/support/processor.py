# -*- coding: utf-8 -*-
#!/usr/bin/env python

def nop(self, *args, **kwargs):
    pass

BaseProcessorMixin = type("BaseProcessorMixin", (object, ), {
    "currentType": lambda *largs: "",
    "allowedTypes": classmethod(lambda cls: ()),
    "managed": lambda *largs: False,
    "beginExecution": nop,
    "endExecution": nop,
    "environmentVariables": nop,
    "shellVariables": nop,
})    

######################### SyntaxProcessor #########################
SyntaxProcessorMixin = type("SyntaxProcessorMixin", (BaseProcessorMixin, ), {
    "allowedTypes": classmethod(lambda cls: ("syntax", )),
    "openTag": nop,
    "closeTag": nop,
    "beginLine": nop,
    "endLine": nop
})

######################### Command Processor #########################
CommandProcessorMixin = type("CommandProcessorMixin", (BaseProcessorMixin, ), {
    "allowedTypes": classmethod(lambda cls: ("command", "dragcommand")),
    #Inputs
    "document": nop,
    "line": nop,
    "character": nop,
    "scope": nop,
    "selection": nop,
    "selectedText": nop,
    "word": nop,
    # beforeRunningCommand
    "saveActiveFile": lambda *largs: True,
    "saveModifiedFiles": lambda *largs: True,
    "nop": lambda *largs: True,
    # Outpu functions
    "replaceInput": nop,
    "atCaret": nop,
    "afterInput": nop,
    "error": nop,
    "discard": nop,
    "replaceSelectedText": nop,
    "replaceSelection": nop,
    "replaceDocument": nop,
    "insertText": nop,
    "afterSelectedText": nop,
    "insertAsSnippet": nop,
    "showAsHTML": nop,
    "showAsTooltip": nop,
    "toolTip": nop,
    "createNewDocument": nop,
    "newWindow": nop,
})

######################### Snipper Processor #########################
SnippetProcessorMixin = type("SnippetProcessorMixin", (BaseProcessorMixin, ), {
    "allowedTypes": classmethod(lambda cls: ("snippet", )),
    "beginRender": nop,
    "endRender": nop,
    "runShellScript": nop,
    # cursor or caret
    "caretPosition": nop,
    # select
    "selectHolder": nop,
    # insert
    "insertText": nop
})

######################### Macro Processor #########################
MacroProcessorMixin = type("MacroProcessorMixin", (BaseProcessorMixin, ), {
    "allowedTypes": classmethod(lambda cls: ("macro", )),
    # Move
    "moveRight": nop,
    "moveLeft": nop,
    "moveUp": nop,
    "moveToEndOfLine": nop,
    "moveToEndOfParagraph": nop,
    "moveToBeginningOfLine": nop,
    "moveToEndOfDocumentAndModifySelection": nop,
    "moveToBeginningOfDocumentAndModifySelection": nop,
    "moveRightAndModifySelection": nop,
    "centerSelectionInVisibleArea": nop,
    "alignLeft": nop,
    # Inserts
    "insertText": nop,
    "insertNewline": nop,
    # Deletes
    "deleteForward": nop,
    "deleteBackward": nop,
    "deleteWordLeft": nop,
    "deleteToBeginningOfLine": nop,
    # Selects
    "selectWord": nop,
    "selectAll": nop,
    "selectHardLine": nop,
    "executeCommandWithOptions": nop,
    "insertSnippetWithOptions": nop,
    "findWithOptions": nop,
    "findNext": nop,
    "indent": nop
})
    
############# Debugs Preocessors ###############
class DebugSyntaxProcessor(SyntaxProcessorMixin):
    def __init__(self, showOutput = True, hashOutput = False):
        self.line_number = 0
        self.printable_line = ''
        self.showOutput = showOutput
        self.hashOutput = hashOutput
        self.hashValue = 0
        
    def pprint(self, line, string, position = 0):
        line = line[:position] + string + line[position:]
        return line

    def openTag(self, name, position):
        if self.showOutput:
            print(self.pprint( '', '{ %d - %s' % (position, name), position + len(self.line_marks)))
        if self.hashOutput:
            self.hashValue = hash("%s:%d:%d" % (name, position, self.hashValue))
            
    def closeTag(self, name, position):
        if self.showOutput:
            print(self.pprint( '', '} %d - %s' % (position, name), position + len(self.line_marks)))
        if self.hashOutput:
            self.hashValue = hash("%s:%d:%d" % (name, position, self.hashValue))

    def beginLine(self, line):
        self.line_number += 1
        self.line_marks = '[%04s] ' % self.line_number
        if self.showOutput:
            print('%s%s' % (self.line_marks, line))

    def beginExecution(self, syntax):
        if self.showOutput:
            print('{%s' % syntax.name)
        if self.hashOutput:
            self.hashValue = hash("%s:%d" % (syntax.name, self.hashValue))
            
    def endExecution(self, syntax):
        if self.showOutput:
            print('}%s' % syntax.name)
        if self.hashOutput:
            self.hashValue = hash("%s:%d" % (syntax.name, self.hashValue))

class DebugSnippetProcessor(SnippetProcessorMixin):
    def __init__(self):
        self.snippet = None
        self.transformation = None
        self.tabreplacement = "\t"
        self.indentation = ""
        self.env = {}

    @property
    def hasSnippet(self):
        return self.snippet is not None
    
    def environmentVariables(self, format = None):
        return self.env
    
    def beginExecution(self, snippet):
        self.snippet = snippet
        self.text = ""
        self.position = 0
    
    def endExecution(self, snippet):
        self.snippet = None
        
    def cursorPosition(self):
        return self.position
            
    def selectHolder(self):
        pass

    def insertText(self, text):
        if self.transformation:
            self.capture += text
        else:
            self.text += text
            self.position += len(text)
