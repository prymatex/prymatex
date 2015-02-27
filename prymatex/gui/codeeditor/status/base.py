#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtCore, QtGui, QtWidgets
from prymatex.core import PrymatexStatusBar
from prymatex.ui.codeeditor.status import Ui_CodeEditorStatus

from ..editor import CodeEditor

from .find import FindMixin
from .findinfiles import FindInFilesMixin
from .replace import ReplaceMixin
from .command import CommandMixin
from .status import StatusMixin

class CodeEditorStatus(PrymatexStatusBar, FindMixin, FindInFilesMixin,
    ReplaceMixin, CommandMixin, StatusMixin, Ui_CodeEditorStatus, QtWidgets.QWidget):
    # ------------------ Flags
    Backward               = CodeEditor.FindBackward
    CaseSensitive          = CodeEditor.FindCaseSensitive
    WholeWord              = CodeEditor.FindWholeWord
    RegularExpression      = CodeEditor.FindRegularExpression
    Wrap                   = 1<<4
    InSelection            = 1<<5
    PreserveCase           = 1<<6
    HighlightMatches       = 1<<7
    ShowContext            = 1<<8
    UseEditor              = 1<<9

    def __init__(self, *args, **kwargs):
        super(CodeEditorStatus, self).__init__(**kwargs)
        self.setupUi(self)
        StatusMixin.setup(self)
        CommandMixin.setup(self)
        self.__flags = QtGui.QTextDocument.FindFlags()
    
    def defaultFlags(self):
        return QtGui.QTextDocument.FindFlags() | self.WholeWord | self.CaseSensitive
        
    def setFlags(self, flags):
        self.__flags = flags

    def flags(self):
        return self.__flags

    def acceptEditor(self, editor):
        return isinstance(editor, CodeEditor)

    def hideAll(self):
        for widget in [self.widgetFind, self.widgetReplace, self.widgetCommand, self.widgetFindInFiles]:
            widget.setVisible(False)
                    
    def initialize(self, *args, **kwargs):
        super(CodeEditorStatus, self).initialize(*args, **kwargs)
        FindMixin.initialize(self, *args, **kwargs)
        FindInFilesMixin.initialize(self, *args, **kwargs)
        ReplaceMixin.initialize(self, *args, **kwargs)
        StatusMixin.initialize(self, *args, **kwargs)
        CommandMixin.initialize(self, *args, **kwargs)
        
        # Connect all finds
        self.comboBoxFind.lineEdit().textChanged.connect(self.on_lineEdit_textChanged)
        self.comboBoxReplaceWhat.lineEdit().textChanged.connect(self.on_lineEdit_textChanged)
        self.comboBoxFindInFilesWhat.lineEdit().textChanged.connect(self.on_lineEdit_textChanged)
        
    # ---------- Tool, set flags and update buttons
    def _update_checked(self, buttons, trigger, checked, flag):
        [ button.setChecked(checked) for button in buttons if trigger != button]
        flags = self.flags()
        if checked:
            flags |= flag
        else:
            flags &= (flag ^ 0xFF)
        self.setFlags(flags)

    # ------- Tool find context        
    def _find_context(self, select=False, update=False):
        editor = self.window().currentEditor()
        cursors = editor.textCursors()
        if select:
            for index, cursor in enumerate(cursors[:]):
                if not cursor.hasSelection(): 
                    _, start, end = editor.wordUnderCursor(cursor, search=True)
                    cursors[index] = editor.newCursorAtPosition(start, end)
        if cursors[0].hasSelection() and update:
            self.comboBoxFind.lineEdit().setText(cursors[0].selectedText())
        return [ editor ] + cursors
    
    # ----------- Signals
    def on_lineEdit_textChanged(self, text):
        combos = [self.comboBoxFind, self.comboBoxReplaceWhat, self.comboBoxFindInFilesWhat]
        for combo in combos:
            if combo.lineEdit() != self.sender():
                combo.lineEdit().blockSignals(True)
                combo.lineEdit().setText(text)
                combo.lineEdit().blockSignals(False)

    def pushButtonRegularExpression_toggled(self, checked):
        self._update_checked(
            [
                self.pushButtonFindRegularExpression,
                self.pushButtonReplaceRegularExpression,
                self.pushButtonFindInFilesRegularExpression
            ], self.sender(), checked, self.RegularExpression
        )
    on_pushButtonFindRegularExpression_toggled = pushButtonRegularExpression_toggled
    on_pushButtonReplaceRegularExpression_toggled = pushButtonRegularExpression_toggled
    on_pushButtonFindInFilesRegularExpression_toggled = pushButtonRegularExpression_toggled
    
    def pushButtonCaseSensitive_toggled(self, checked):
        self._update_checked(
            [
                self.pushButtonFindCaseSensitive,
                self.pushButtonReplaceCaseSensitive,
                self.pushButtonFindInFilesCaseSensitive
            ], self.sender(), checked, self.CaseSensitive
        )
    on_pushButtonFindCaseSensitive_toggled = pushButtonCaseSensitive_toggled
    on_pushButtonReplaceCaseSensitive_toggled = pushButtonCaseSensitive_toggled
    on_pushButtonFindInFilesCaseSensitive_toggled = pushButtonCaseSensitive_toggled
    
    def pushButtonWholeWord_toggled(self, checked):
        self._update_checked(
            [
                self.pushButtonFindWholeWord,
                self.pushButtonReplaceWholeWord,
                self.pushButtonFindInFilesWholeWord
            ], self.sender(), checked, self.WholeWord
        )
    on_pushButtonFindWholeWord_toggled = pushButtonWholeWord_toggled
    on_pushButtonReplaceWholeWord_toggled = pushButtonWholeWord_toggled
    on_pushButtonFindInFilesWholeWord_toggled = pushButtonWholeWord_toggled
    
    def pushButtonWrap_toggled(self, checked):
        self._update_checked(
            [
                self.pushButtonFindWrap,
                self.pushButtonReplaceWrap
            ], self.sender(), checked, self.Wrap
        )
    on_pushButtonFindWrap_toggled = pushButtonWrap_toggled
    on_pushButtonReplaceWrap_toggled = pushButtonWrap_toggled
    
    def pushButtonInSelection_toggled(self, checked):
        self._update_checked(
            [
                self.pushButtonFindInSelection,
                self.pushButtonReplaceInSelection
            ], self.sender(), checked, self.InSelection
        )
    on_pushButtonFindInSelection_toggled = pushButtonInSelection_toggled
    on_pushButtonReplaceInSelection_toggled = pushButtonInSelection_toggled
    
    def pushButtonHighlightMatches_toggled(self, checked):
        self._update_checked(
            [
                self.pushButtonFindHighlightMatches,
                self.pushButtonReplaceHighlightMatches
            ], self.sender(), checked, self.HighlightMatches
        )
    on_pushButtonFindHighlightMatches_toggled = pushButtonHighlightMatches_toggled
    on_pushButtonReplaceHighlightMatches_toggled = pushButtonHighlightMatches_toggled
        
    def on_pushButtonReplacePreserveCase_toggled(self, checked):
        self._update_checked(
            [], self.sender(), checked, self.PreserveCase
        )
    
    def on_pushButtonFindInFilesShowContext_toggled(self, checked):
        self._update_checked(
            [], self.sender(), checked, self.ShowContext
        )
    
    def on_pushButtonFindInFilesUseEditor_toggled(self, checked):
        self._update_checked(
            [], self.sender(), checked, self.UseEditor
        )
    
    # ------------- Contributes to Main Menu
    @classmethod
    def contributeToMainMenu(cls):
        menu = {}
        menu["find"] = {
            'before': 'view',
            'icon': None,
            'name': 'find',
            'text': 'F&ind',
            'items': [
                {'text': "Find...",
                 'sequence': ("StatusBar", "Find", "Find"),
                 'triggered': lambda st, checked=False: st.find()
                },
                {'text': "Find Next",
                 'sequence': ("StatusBar", "FindNext", "F3"),
                 'triggered': lambda st, checked=False: st.findNext()
                },
                {'text': "Find Previous",
                 'sequence': ("StatusBar", "FindPrevious", "Shift+F3"),
                 'triggered': lambda st, checked=False: st.findPrevious()
                },
                {'text': "Incremental Find",
                 'sequence': ("StatusBar", "IncrementalFind", "Ctrl+I"),
                 'triggered': lambda st, checked=False: st.incrementalFind()
                }, '-',
                {'text': "Replace",
                 'sequence': ("StatusBar", "Replace", "Replace"),
                 'triggered': lambda st, checked=False: st.replace()
                },
                {'text': "Replace Next",
                 'sequence': ("StatusBar", "ReplaceNext", "Ctrl+Shift+H"),
                 'triggered': lambda st, checked=False: st.replaceNext()
                }, '-',
                {'text': "Quick Find",
                 'sequence': ("StatusBar", "QuickFind", "Ctrl+F3"),
                 'triggered': lambda st, checked=False: st.quickFind()
                },
                {'text': "Quick Find All",
                 'sequence': ("StatusBar", "QuickFindAll", "Alt+F3"),
                 'triggered': lambda st, checked=False: st.quickFindAll()
                },
                {'text': "Quick Add Next",
                 'sequence': ("StatusBar", "QuickAddNext", "Ctrl+D"),
                 'triggered': lambda st, checked=False: st.quickAddNext()
                },
                {'text': "Quick Skip Next",
                 'triggered': lambda st, checked=False: st.quickSkipNext()
                }, '-',
                {'text': "Use Selection For Find",
                 'sequence': ("StatusBar", "UseSelectionForFind", "Ctrl+E"),
                 'triggered': lambda st, checked=False: st.showFindReplace()
                },
                {'text': "Use Selection For Replace",
                 'sequence': ("StatusBar", "UseSelectionForReplace", "Ctrl+Shift+E"),
                 'triggered': lambda st, checked=False: st.showFindReplace()
                }, '-',
                {'text': "Find In Files",
                 'sequence': ("StatusBar", "FindInFiles", "Ctrl+Shift+F"),
                 'triggered': lambda st, checked=False: st.findInFiles()
                },
                {'text': "Find Results",
                 'items': [
                     {'text': "Show Results Panel",
                      'triggered': lambda st, checked=False: st.showFindReplace()
                     },
                     {'text': "Next Result",
                      'sequence': ("StatusBar", "NextResult", "F4"),
                      'triggered': lambda st, checked=False: st.showFindReplace()
                     },
                     {'text': "Previous Result",
                      'sequence': ("StatusBar", "PreviousResult", "Shift+F4"),
                      'triggered': lambda st, checked=False: st.showFindReplace()
                    }]
                }]
            }
        menu["text"] = [
                {'text': 'Filter through command',
                 'triggered': lambda st, checked=False: st.filterThroughCommand()
                 }
            ]
        return menu

    def contributeToShortcuts(self):
        return [{
            'sequence': ("StatusBar", "QuickAddPrevious", "Ctrl+Shift+D"),
            'activated': self.quickAddPrevious
        }]