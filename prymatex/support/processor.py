# -*- coding: utf-8 -*-
#!/usr/bin/env python

def nop(self, *args):
    pass

def return_true(self, *args):
    return True
    
######################### SyntaxProcessor #########################

PMXSyntaxProcessor = type("PMXSyntaxProcessor", (object, ), {
    "startParsing": nop,
    "endParsing": nop,
    "openTag": nop,
    "closeTag": nop,
    "beginLine": nop,
    "endLine": nop
})

######################### Command Processor #########################
PMXCommandProcessor = type("PMXCommandProcessor", (object, ), {
    "startCommand": nop,
    "endCommand": nop,
    "environmentVariables": nop,
    #Inputs
    "document": nop,
    "line": nop,
    "character": nop,
    "scope": nop,
    "selection": nop,
    #"selectedText": nop,
    "word": nop,
    # beforeRunningCommand
    "saveActiveFile": return_true,
    "saveModifiedFiles": return_true,
    "nop": return_true,
    # deleteFromEditor
    "deleteWord": nop,
    "deleteSelection": nop,
    "deleteCharacter": nop,
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
PMXSnippetProcessor = type("PMXSnippetProcessor", (object, ), {
    "startSnippet": nop,
    "endSnippet": nop,
    "startRender": nop,
    "endRender": nop,
    "environmentVariables": nop,
    # transformations
    "startTransformation": nop,
    "endTransformation": nop,
    # cursor or caret
    "caretPosition": nop,
    # select
    "selectHolder": nop,
    # insert
    "insertText": nop
})

######################### Macro Processor #########################
PMXMacroProcessor = type("PMXMacroProcessor", (object, ), {
    "startMacro": nop,
    "endMacro": nop,
    "environmentVariables": nop,
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
class PMXDebugSyntaxProcessor(PMXSyntaxProcessor):
    def __init__(self):
        self.line_number = 0
        self.printable_line = ''

    def pprint(self, line, string, position = 0):
        line = line[:position] + string + line[position:]
        return line

    def openTag(self, name, position):
        print self.pprint( '', '{ %d - %s' % (position, name), position + len(self.line_marks))

    def closeTag(self, name, position):
        print self.pprint( '', '} %d - %s' % (position, name), position + len(self.line_marks))

    def beginLine(self, line):
        self.line_number += 1
        self.line_marks = '[%04s] ' % self.line_number
        print '%s%s' % (self.line_marks, line)

    def startParsing(self, name):
        print '{%s' % name

    def endParsing(self, name):
        print '}%s' % name

class PMXDebugSnippetProcessor(PMXSnippetProcessor):
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
    
    def startSnippet(self, snippet):
        self.snippet = snippet
        self.text = ""
        self.position = 0
    
    def endSnippet(self):
        self.snippet = None
    
    def startTransformation(self, transformation):
        self.transformation = True
        self.capture = ""
        
    def endTransformation(self, transformation):
        self.transformation = False
        text = transformation.transform(self.capture)
        self.insertText(text)
        
    def cursorPosition(self):
        return self.position
            
    def selectHolder(self, holder):
        pass

    def insertText(self, text):
        if self.transformation:
            self.capture += text
        else:
            self.text += text
            self.position += len(text)