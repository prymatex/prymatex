#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtCore, QtGui, QtWidgets
from prymatex.core import PrymatexStatusBar
from prymatex.ui.codeeditor.newstatus import Ui_CodeEditorStatus

from ..editor import CodeEditor

from .find import FindMixin
from .findinfiles import FindInFilesMixin
from .replace import ReplaceMixin
from .command import CommandMixin
from .status import StatusMixin

class CodeEditorStatus(PrymatexStatusBar, FindMixin, FindInFilesMixin,
    ReplaceMixin, CommandMixin, StatusMixin, Ui_CodeEditorStatus, QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(CodeEditorStatus, self).__init__(**kwargs)
        self.setupUi(self)
        StatusMixin.setup(self)

    def acceptEditor(self, editor):
        return isinstance(editor, CodeEditor)
        
    def initialize(self, *args, **kwargs):
        super(CodeEditorStatus, self).initialize(*args, **kwargs)
        FindMixin.initialize(self, *args, **kwargs)
        FindInFilesMixin.initialize(self, *args, **kwargs)
        ReplaceMixin.initialize(self, *args, **kwargs)
        StatusMixin.initialize(self, *args, **kwargs)
        CommandMixin.initialize(self, *args, **kwargs)

    # ------------- Contributes to Main Menu
    @classmethod
    def contributeToMainMenu(cls):
        menu = {}
        menu["edit"] = {
            'before': 'mode',
            'name': 'find',
            'text': '&Find',
            'items': [
                {'text': "Find...",
                 'sequence': ("StatusBar", "Find", "Find"),
                 'triggered': lambda st, checked=False: st.showFind()
                },
                {'text': "Find Next",
                 'sequence': ("StatusBar", "FindNext", "F3"),
                 'triggered': lambda st, checked=False: st.showIFind()
                },
                {'text': "Find Previous",
                 'sequence': ("StatusBar", "FindPrevious", "Shift+F3"),
                 'triggered': lambda st, checked=False: st.showIFind()
                },
                {'text': "Incremental Find",
                 'sequence': ("StatusBar", "IncrementalFind", "Ctrl+I"),
                 'triggered': lambda st, checked=False: st.showIFind()
                }, '-',
                {'text': "Replace",
                 'sequence': ("StatusBar", "Replace", "Replace"),
                 'triggered': lambda st, checked=False: st.showReplace()
                },
                {'text': "Replace Next",
                 'sequence': ("StatusBar", "ReplaceNext", "Ctrl+Shift+H"),
                 'triggered': lambda st, checked=False: st.showReplace()
                }, '-',
                {'text': "Quick Find",
                 'sequence': ("StatusBar", "QuickFind", "Ctrl+F3"),
                 'triggered': lambda st, checked=False: st.showFindReplace()
                },
                {'text': "Quick Find All",
                 'sequence': ("StatusBar", "QuickFindAll", "Alt+F3"),
                 'triggered': lambda st, checked=False: st.showFindReplace()
                },
                {'text': "Quick Add Next",
                 'sequence': ("StatusBar", "QuickAddNext", "Ctrl+D"),
                 'triggered': lambda st, checked=False: st.showFindReplace()
                },
                {'text': "Quick Skip Next",
                 'triggered': lambda st, checked=False: st.showFindReplace()
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
                 'triggered': lambda st, checked=False: st.showFindInFiles()
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
                 'triggered': lambda st, checked=False: st.showCommand()
                 }
            ]
        return menu
