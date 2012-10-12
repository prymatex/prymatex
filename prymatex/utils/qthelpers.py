#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Qt utilities

Come from Spyder
Source code (spyderlib/utils/qthelpers.py) Copyright © 2009-2010 Pierre Raybaut
Licensed under the terms of the MIT License
"""

import os, re
import os.path as osp

from prymatex.qt import QtCore, QtGui

# Local import
import prymatex
from prymatex import resources
from prymatex.utils import programs

def qapplication(translate=True):
    """Return QApplication instance creates it if it doesn't already exist"""
    app = QtGui.QApplication.instance()
    if not app:
        app = QtGui.QApplication([])
        # Set Application name for Gnome 3 (https://groups.google.com/forum/#!topic/pyside/24qxvwfrRDs)
        app.setApplicationName(prymatex.__name__.title())
    if translate:
        install_translator(app)
    return app

def file_uri(fname):
    """Select the right file uri scheme according to the operating system"""
    if os.name == 'nt':
        # Local file
        if re.search(r'^[a-zA-Z]:', fname):
            return 'file:///' + fname
        # UNC based path
        else:
            return 'file://' + fname
    else:
        return 'file://' + fname

QT_TRANSLATOR = None
def install_translator(qapp):
    """Install Qt translator to the QApplication instance"""
    global QT_TRANSLATOR
    if QT_TRANSLATOR is None:
        qt_translator = QtCore.QTranslator()
        if qt_translator.load("qt_"+QtCore.QLocale.system().name(),
                      QtCore.QLibraryInfo.location(QtCore.QLibraryInfo.TranslationsPath)):
            QT_TRANSLATOR = qt_translator # Keep reference alive
    if QT_TRANSLATOR is not None:
        qapp.installTranslator(QT_TRANSLATOR)


def keybinding(attr):
    """Return keybinding"""
    ks = getattr(QtGui.QKeySequence, attr)
    return QtGui.QKeySequence.keyBindings(ks)[0]


def _process_mime_path(path, extlist):
    if path.startswith(r"file://"):
        if os.name == 'nt':
            # On Windows platforms, a local path reads: file:///c:/...
            # and a UNC based path reads like: file://server/share
            if path.startswith(r"file:///"): # this is a local path
                path=path[8:]
            else: # this is a unc path
                path = path[5:]
        else:
            path = path[7:]
    if osp.exists(path):
        if extlist is None or osp.splitext(path)[1] in extlist:
            return path


def mimedata2url(source, extlist=None):
    """
    Extract url list from MIME data
    extlist: for example ('.py', '.pyw')
    """
    pathlist = []
    if source.hasUrls():
        for url in source.urls():
            path = _process_mime_path(unicode(url.toString()), extlist)
            if path is not None:
                pathlist.append(path)
    elif source.hasText():
        for rawpath in unicode(source.text()).splitlines():
            path = _process_mime_path(rawpath, extlist)
            if path is not None:
                pathlist.append(path)
    if pathlist:
        return pathlist


def keyevent2tuple(event):
    """Convert QKeyEvent instance into a tuple"""
    return (event.type(), event.key(), event.modifiers(), event.text(),
            event.isAutoRepeat(), event.count())

    
def tuple2keyevent(past_event):
    """Convert tuple into a QKeyEvent instance"""
    return QtGui.QKeyEvent(*past_event)


def restore_keyevent(event):
    if isinstance(event, tuple):
        _, key, modifiers, text, _, _ = event
        event = tuple2keyevent(event)
    else:
        text = event.text()
        modifiers = event.modifiers()
        key = event.key()
    ctrl = modifiers & QtCore.Qt.ControlModifier
    shift = modifiers & QtCore.Qt.ShiftModifier
    return event, text, key, ctrl, shift


def create_toolbutton(parent, text=None, shortcut=None, icon=None, tip=None,
                      toggled=None, triggered=None,
                      autoraise=True, text_beside_icon=False):
    """Create a QToolButton"""
    button = QtGui.QToolButton(parent)
    if text is not None:
        button.setText(text)
    if icon is not None:
        if isinstance(icon, (str, unicode)):
            icon = resources.getIcon(icon)
        button.setIcon(icon)
    if text is not None or tip is not None:
        button.setToolTip(text if tip is None else tip)
    if text_beside_icon:
        button.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
    button.setAutoRaise(autoraise)
    if triggered is not None:
        QtCore.QObject.connect(button, QtCore.SIGNAL('clicked()'), triggered)
    if toggled is not None:
        QtCore.QObject.connect(button, QtCore.SIGNAL("toggled(bool)"), toggled)
        button.setCheckable(True)
    if shortcut is not None:
        button.setShortcut(shortcut)
    return button


def action2button(action, autoraise=True, text_beside_icon=False, parent=None):
    """Create a QToolButton directly from a QAction object"""
    if parent is None:
        parent = action.parent()
    button = QtGui.QToolButton(parent)
    button.setDefaultAction(action)
    button.setAutoRaise(autoraise)
    if text_beside_icon:
        button.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
    return button


def toggle_actions(actions, enable):
    """Enable/disable actions"""
    if actions is not None:
        for action in actions:
            if action is not None:
                action.setEnabled(enable)


def create_action(parent, text, shortcut=None, icon=None, tip=None,
                  toggled=None, triggered=None, data=None, menurole=None,
                  context=QtCore.Qt.WindowShortcut):
    """Create a QAction"""
    action = QtGui.QAction(text, parent)
    if triggered is not None:
        parent.connect(action, QtCore.SIGNAL("triggered()"), triggered)
    if toggled is not None:
        parent.connect(action, QtCore.SIGNAL("toggled(bool)"), toggled)
        action.setCheckable(True)
    if icon is not None:
        if isinstance(icon, (str, unicode)):
            icon = resources.getIcon(icon)
        action.setIcon(icon)
    if shortcut is not None:
        action.setShortcut(shortcut)
    if tip is not None:
        action.setToolTip(tip)
        action.setStatusTip(tip)
    if data is not None:
        action.setData(data)
    if menurole is not None:
        action.setMenuRole(menurole)
    #TODO: Hard-code all shortcuts and choose context=QtCore.Qt.WidgetShortcut
    # (this will avoid calling shortcuts from another dockwidget
    #  since the context thing doesn't work quite well with these widgets)
    action.setShortcutContext(context)
    return action


def add_actions(target, actions, insert_before=None):
    """Add actions to a menu"""
    previous_action = None
    target_actions = list(target.actions())
    if target_actions:
        previous_action = target_actions[-1]
        if previous_action.isSeparator():
            previous_action = None
    for action in actions:
        if (action is None) and (previous_action is not None):
            if insert_before is None:
                target.addSeparator()
            else:
                target.insertSeparator(insert_before)
        elif isinstance(action, QtGui.QMenu):
            if insert_before is None:
                target.addMenu(action)
            else:
                target.insertMenu(insert_before, action)
        elif isinstance(action, QtGui.QAction):
            if insert_before is None:
                target.addAction(action)
            else:
                target.insertAction(insert_before, action)
        previous_action = action


def get_item_user_text(item):
    """Get QTreeWidgetItem user role string"""
    return item.data(0, QtCore.Qt.UserRole)


def set_item_user_text(item, text):
    """Set QTreeWidgetItem user role string"""
    item.setData(0, QtCore.Qt.UserRole, text)


def create_bookmark_action(parent, url, title, icon=None, shortcut=None):
    """Create bookmark action"""
    if icon is None:
        icon = resources.getIcon('browser.png')
    return create_action( parent, title, shortcut=shortcut, icon=icon,
                          triggered=lambda u=url: programs.start_file(u) )


def create_module_bookmark_actions(parent, bookmarks):
    """
    Create bookmark actions depending on module installation:
    bookmarks = ((module_name, url, title), ...)
    """
    actions = []
    for key, url, title, icon in bookmarks:
        if programs.is_module_installed(key):
            act = create_bookmark_action(parent, url, title, resources.getIcon(icon))
            actions.append(act)
    return actions

        
def create_program_action(parent, text, icon, name, nt_name=None):
    """Create action to run a program"""
    if isinstance(icon, basestring):
        icon = resources.getIcon(icon)
    if os.name == 'nt' and nt_name is not None:
        name = nt_name
    path = programs.find_program(name)
    if path is not None:
        return create_action(parent, text, icon=icon,
                             triggered=lambda: programs.run_program(name))

        
def create_python_script_action(parent, text, icon, package, module, args=[]):
    """Create action to run a GUI based Python script"""
    if isinstance(icon, basestring):
        icon = resources.getIcon(icon)
    if programs.python_script_exists(package, module):
        return create_action(parent, text, icon=icon,
                             triggered=lambda:
                             programs.run_python_script(package, module, args))


class DialogManager(QtCore.QObject):
    """
    Object that keep references to non-modal dialog boxes for another QObject,
    typically a QMainWindow or any kind of QWidget
    """
    def __init__(self):
        QtCore.QObject.__init__(self)
        self.dialogs = {}
        
    def show(self, dialog):
        """Generic method to show a non-modal dialog and keep reference
        to the QtCore.Qt C++ object"""
        for dlg in self.dialogs.values():
            if unicode(dlg.windowTitle()) == unicode(dialog.windowTitle()):
                dlg.show()
                dlg.raise_()
                break
        else:
            dialog.show()
            self.dialogs[id(dialog)] = dialog
            self.connect(dialog, QtCore.SIGNAL('accepted()'),
                         lambda eid=id(dialog): self.dialog_finished(eid))
            self.connect(dialog, QtCore.SIGNAL('rejected()'),
                         lambda eid=id(dialog): self.dialog_finished(eid))
        
    def dialog_finished(self, dialog_id):
        """Manage non-modal dialog boxes"""
        return self.dialogs.pop(dialog_id)
    
    def close_all(self):
        """Close all opened dialog boxes"""
        for dlg in self.dialogs.values():
            dlg.reject()

        
def get_std_icon(name, size=None):
    """Get standard platform icon
    Call 'show_std_icons()' for details"""
    if not name.startswith('SP_'):
        name = 'SP_'+name
    icon = QtGui.QWidget().style().standardIcon( getattr(QtGui.QStyle, name) )
    if size is None:
        return icon
    else:
        return QtGui.QIcon( icon.pixmap(size, size) )


def get_filetype_icon(fname):
    """Return file type icon"""
    ext = osp.splitext(fname)[1]
    if ext.startswith('.'):
        ext = ext[1:]
    return resources.getIcon( "%s.png" % ext, get_std_icon('FileIcon') )


class ShowStdIcons(QtGui.QWidget):
    """
    Dialog showing standard icons
    """
    def __init__(self, parent):
        QtGui.QWidget.__init__(self, parent)
        layout = QtGui.QHBoxLayout()
        row_nb = 14
        cindex = 0
        for child in dir(QtGui.QStyle):
            if child.startswith('SP_'):
                if cindex == 0:
                    col_layout = QtGui.QVBoxLayout()
                icon_layout = QtGui.QHBoxLayout()
                icon = get_std_icon(child)
                label = QtGui.QLabel()
                label.setPixmap(icon.pixmap(32, 32))
                icon_layout.addWidget( label )
                icon_layout.addWidget( QtGui.QLineEdit(child.replace('SP_', '')) )
                col_layout.addLayout(icon_layout)
                cindex = (cindex+1) % row_nb
                if cindex == 0:
                    layout.addLayout(col_layout)                    
        self.setLayout(layout)
        self.setWindowTitle('Standard Platform Icons')
        self.setWindowIcon(get_std_icon('TitleBarMenuButton'))


def show_std_icons():
    """
    Show all standard Icons
    """
    app = qapplication()
    dialog = ShowStdIcons(None)
    dialog.show()
    import sys
    sys.exit(app.exec_())


if __name__ == "__main__":
    show_std_icons()