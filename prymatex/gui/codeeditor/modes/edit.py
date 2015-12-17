#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from prymatex.qt import QtCore, QtGui, QtWidgets
from prymatex.qt.helpers import keyevent_to_keysequence

from .base import CodeEditorBaseMode

class CodeEditorEditMode(CodeEditorBaseMode):
    def name(self):
        return self.editor.overwriteMode() and "OVERWRITE" or "EDIT"

    def initialize(self, **kwargs):
        super(CodeEditorEditMode, self).initialize(**kwargs)
        self.registerKeyPressHandler(QtCore.Qt.Key_Return, self.__insert_new_line)
        self.registerKeyPressHandler(QtCore.Qt.Key_Tab, self.__insert_tab_bundle_item)
        self.registerKeyPressHandler(QtCore.Qt.Key_Home, self.__move_cursor_to_home)
        self.registerKeyPressHandler(QtCore.Qt.Key_End, self.__move_cursor_to_end)
        self.registerKeyPressHandler(QtCore.Qt.Key_Backspace, self.__backspace_behavior)
        self.registerKeyPressHandler(QtCore.Qt.Key_Delete, self.__delete_behavior)
        self.registerKeyPressHandler(QtCore.Qt.Key_Insert, self.__toggle_overwrite)
        self.editor.queryCompletions.connect(self.on_editor_queryCompletions)

    # OVERRIDE: CodeEditorBaseMode.keyPress_handlers()
    def keyPress_handlers(self, event):
        for handler in super().keyPress_handlers(event):
            yield handler

        # Bundle items 
        sequence = keyevent_to_keysequence(event)
        if sequence in self.application().supportManager.getAllKeySequences():
            yield lambda event, sequence=sequence: \
                self.__insert_key_bundle_item(event, sequence)

        # Pairs
        settings = self.editor.currentPreferenceSettings()
        character = event.text()
        if any((pair for pair in settings.smartTypingPairs if character in pair)):
            yield lambda event, settings=settings, character=character: \
                self.__insert_typing_pairs(event, settings, character)

        #if event.text():
        #    self.editor.runCommand("insert", characters=event.text())
        
    # ------------ Key press handlers
    def __insert_new_line(self, event):
        self.editor.runCommand("insert", characters = '\n')
        return True
    
    def __insert_key_bundle_item(self, event, sequence):
        leftScope, rightScope = self.editor.scope(self.editor.textCursor())
        items = self.application().supportManager.getKeySequenceItem(
            sequence, leftScope, rightScope)
        self.editor.insertBundleItem(items)
        return bool(items)
    
    def __insert_tab_bundle_item(self, event):
        cursor = self.editor.textCursor()
        if not cursor.hasSelection():
            trigger = self.application().supportManager.getTabTriggerSymbol(cursor.block().text(), cursor.positionInBlock())
            if trigger:
                triggerCursor = self.editor.newCursorAtPosition(
                    cursor.position(), cursor.position() - len(trigger))
                leftScope, rightScope = self.editor.scope(triggerCursor)
                items = self.application().supportManager.getTabTriggerItem(
                    trigger, leftScope, rightScope)
                self.editor.insertBundleItem(items, textCursor=triggerCursor)
                return bool(items)

    def __move_cursor_to_home(self, event):
        cursor = self.editor.textCursor()
        block = cursor.block()
        newPosition = block.position() + len(self.editor.blockIndentation(block))
        # Solo si el cursor no esta al final de la indentacion
        if newPosition != cursor.position():
            cursor.setPosition(newPosition, event.modifiers() == QtCore.Qt.ShiftModifier and QtGui.QTextCursor.KeepAnchor or QtGui.QTextCursor.MoveAnchor)
            self.editor.setTextCursor(cursor)
            return True
        
    def __move_cursor_to_end(self, event):
        cursor = self.editor.textCursor()
        block = cursor.block()
        newPosition = block.position() + len(block.text().rstrip())
        # Solo si el cursor no esta al final del texto
        if newPosition != cursor.position():
            cursor.setPosition(newPosition, event.modifiers() == QtCore.Qt.ShiftModifier and QtGui.QTextCursor.KeepAnchor or QtGui.QTextCursor.MoveAnchor)
            self.editor.setTextCursor(cursor)
            return True

    def __backspace_behavior(self, event):
        self.editor.runCommand("left_delete")
        return True

    def __delete_behavior(self, event):
        self.editor.runCommand("right_delete")
        return True
        
    def __insert_typing_pairs(self, event, settings, character):
        pair = [pair for pair in settings.smartTypingPairs if character in pair][0]

        cursor = self.editor.textCursor()
        cl, cr, clo, cro = self.editor._smart_typing_pairs(cursor)
        
        isOpen = character == pair[0]
        isClose = character == pair[1]
        control_down = bool(event.modifiers() & QtCore.Qt.ControlModifier)
        if isClose and not cursor.hasSelection() \
            and cr and cro and character == cr.selectedText():
            # Skip
            cursor.movePosition(QtGui.QTextCursor.NextCharacter)
            self.editor.setTextCursor(cursor)
            return True
        elif control_down and isOpen:
            if cursor.hasSelection():
                selectedText = cursor.selectedText()
                if any([selectedText == pair[0] for pair in settings.smartTypingPairs]):
                    # Replace
                    if cl is not None and clo is not None:
                        cl.insertText(pair[0])
                        clo.insertText(pair[1])
                    elif cr is not None and cro is not None:
                        cr.insertText(pair[0])
                        cro.insertText(pair[1])
                else:
                    # Wrap
                    cursor.insertText("%s%s%s" % (pair[0],selectedText,pair[1]))
                return True
            else:
                if cl and clo:
                    if cursor.position() == cl.selectionStart():
                        cl.setPosition(cl.selectionStart())
                        clo.setPosition(clo.selectionEnd())
                    else:
                        cl.setPosition(cl.selectionEnd())
                        clo.setPosition(clo.selectionStart())
                    cursor.beginEditBlock()
                    cl.insertText(pair[0])
                    clo.insertText(pair[1])
                    cursor.endEditBlock()
                    return True
                elif cr and cro:
                    if cursor.position() == cr.selectionStart():
                        cr.setPosition(cr.selectionStart())
                        cro.setPosition(cro.selectionEnd())
                    else:
                        cr.setPosition(cr.selectionEnd())
                        cro.setPosition(cro.selectionStart())
                    cursor.beginEditBlock()
                    cr.insertText(pair[0])
                    cro.insertText(pair[1])
                    cursor.endEditBlock()
                    return True
                    
        word, wordStart, wordEnd = self.editor.currentWord()
        if isOpen and not (wordStart <= cursor.position() < wordEnd):
            self.editor.insertSnippet("%s$0%s" % (pair[0], pair[1]))
            return True

    def __toggle_overwrite(self, event):
        self.editor.setOverwriteMode(not self.editor.overwriteMode())

    def on_editor_queryCompletions(self, automatic):
        alreadyTyped, start, end = self.editor.textUnderCursor(direction="left", search = True)
        if alreadyTyped or not automatic:
            leftScope, rightScope = self.editor.scope(self.editor.textCursor())
            # Suggestions
            words = self.editor.extractCompletions(alreadyTyped)
            words += self.editor.currentPreferenceSettings().completions
            items = self.editor.application().supportManager.getAllTabTriggerItemsByScope(leftScope, rightScope)
            triggers = {item.tabTrigger: item for item in items if item.tabTrigger.startswith(alreadyTyped)}
            suggestions = sorted(set(words + list(triggers.keys())))
            def suggestions_generator(suggestions, words, triggers):
                def _generator():
                    for suggestion in suggestions:
                        # Is bundle item
                        if suggestion in triggers:
                            item = triggers[suggestion]
                            yield {
                                "icon": self.editor.resources().get_icon("bundle-item-%s" % item.type()),
                                "match": suggestion,
                                "tool_tip": "%s - %s" % (item.name, item.bundle.name),
                                "display": "%s(%s)" % (suggestion, item.name),
                                "item": item
                            }
                        if suggestion in words:
                            yield ("%s" % suggestion, suggestion)
                return _generator()
            if suggestions:
                self.editor.showCompletionWidget(
                    suggestions_generator(suggestions, words, triggers),
                    automatic
                )
