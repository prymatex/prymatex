#!/usr/bin/env python
from prymatex.core import constants

class CodeEditorCommandsMixin(object):
    def command_insert(self, characters):
        cursor = self.textCursor()
        tab_behavior = self.tabKeyBehavior()
        current_text = cursor.block().text()[:cursor.positionInBlock()]
        current_indentation = self.blockIndentation(cursor.block())        
        cursor.beginEditBlock()
        
        for text in characters.splitlines(True):
            settings = self.preferenceSettings(cursor)
            flag = settings.indentationFlag(
                current_text + text[:-1]
            )
            
            if flag is constants.INDENT_INCREASE:
                self.logger().debug("Increase indentation")
                new_indentation = current_indentation + tab_behavior
            elif flag is constants.INDENT_NEXTLINE:
                #TODO: Creo que este no es el correcto
                self.logger().debug("Increase next line indentation")
                new_indentation = current_indentation + tab_behavior
            elif flag is constants.INDENT_UNINDENT:
                self.logger().debug("Unindent")
                new_indentation = ""
            elif flag is constants.INDENT_DECREASE:
                self.logger().debug("Decrease indentation")
                new_indentation = current_indentation[:-len(tab_behavior)]
            else:
                self.logger().debug("Preserve indentation")
                new_indentation = current_indentation[:cursor.positionInBlock()]
            cursor.insertText(
                text.replace('\n', "\n%s" % new_indentation)
            )
            current_text = "%s" % new_indentation
            current_indentation = new_indentation
        cursor.endEditBlock()
        self.ensureCursorVisible()

    def command_left_delete(self):
        cursor = self.textCursor()
        if not cursor.hasSelection():
            # TODO Quiza esto sea una macro
            # ----------- Remove Braces
            cl, cr, clo, cro = self._smart_typing_pairs(cursor)
            if cl and clo  and (cl.selectionStart() == clo.selectionEnd() or cl.selectionEnd() == clo.selectionStart()):
                cursor.beginEditBlock()
                cl.removeSelectedText()
                clo.removeSelectedText()
                cursor.endEditBlock()
                return
            
            # ----------- Remove Tab_behavior
            tab_behavior = self.tabKeyBehavior()
            ncursor = self.newCursorAtPosition(cursor.position(), cursor.position() - len(tab_behavior))
            if ncursor.selectedText() == tab_behavior:
                ncursor.removeSelectedText()
                return
        cursor.deletePreviousChar()

    def command_right_delete(self):
        cursor = self.textCursor()
        if not cursor.hasSelection():
            # ----------- Remove Braces
            cl, cr, clo, cro = self._smart_typing_pairs(cursor)
            if cr and cro  and (cr.selectionStart() == cro.selectionEnd() or cr.selectionEnd() == cro.selectionStart()):
                cursor.beginEditBlock()
                cr.removeSelectedText()
                cro.removeSelectedText()
                cursor.endEditBlock()
                return
            # ----------- Remove Tab_behavior
            tab_behavior = self.tabKeyBehavior()
            ncursor = self.newCursorAtPosition(cursor.position(), cursor.position() + len(tab_behavior))
            if ncursor.selectedText() == tab_behavior:
                ncursor.removeSelectedText()
                return
        cursor.deleteChar()

    def command_auto_complete(self, *args, **kwargs):
        self._query_completions(True)
        
    def command_hide_auto_complete(self):
        self.hideCompletionWidget()