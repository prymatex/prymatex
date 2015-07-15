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
