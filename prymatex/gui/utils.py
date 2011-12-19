#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import string

from PyQt4 import QtGui, QtCore

from prymatex.utils.i18n import ugettext as _

"""
Algunas definciones en Python para tareas de Gui
"""

to_ascii = lambda s: filter(lambda c: c in string.ascii_letters, s)
to_ascii_cap = lambda s: to_ascii(s).capitalize()

def centerWidget(widget, scale = None):
    """
    Center de widget in the screen
    Scale is a tuple with width and height ex: (0.7, 0.65)
    """
    screen = QtGui.QDesktopWidget().screenGeometry()
    if scale is not None:
        widget.resize(screen.width() * scale[0], screen.height() * scale[1])
    widget.move((screen.width() - widget.size().width()) / 2, (screen.height() - widget.size().height()) / 2)
    
def text_to_object_name(text, sufix = None):
    """
    &Text Button name -> TextButtonName%{sufix}
    """
    words = text.split(' ')
    name = ''.join(map(to_ascii_cap, words))
    if prefix:
        name = prefix + name
    return name

def createButton(parent, text, shortcut = None, object_name = None, do_i18n = False, **opts):
    text = do_i18n and _(text) or text
    if shortcut:
        shortcut = do_i18n and _(shortcut) or shortcut
    
    button = QPushButton(text, parent)
    if not object_name:
        object_name = text_to_object_name(text, 'button')
    button.setObjectName(object_name)
    #buttons.setKey
    button.setFlat(True)
    setattr(parent, object_name, button)
    return button


_available_keys = filter(lambda s: s.startswith('Key_'), dir(QtCore.Qt))
KEYS_DICT = dict([(name[4:], getattr(QtCore.Qt, name)) for name in _available_keys])
KEYS_DICT.update({'Ctrl': QtCore.Qt.CTRL, 'Control': QtCore.Qt.CTRL, 'CTRL': QtCore.Qt.CTRL, 
                  'Shift': QtCore.Qt.SHIFT, 'Shift': QtCore.Qt.SHIFT,
                  'Alt': QtCore.Qt.ALT, 'ALT': QtCore.Qt.ALT,
                  'Meta': QtCore.Qt.META, 'META': QtCore.Qt.META,
                  })


def text_to_KeySequence(text):
    try:
        ints = [ KEYS_DICT[k] for k in text.split('+') ]
        ks = QKeySequence(sum(ints))
        #ks = QKeySequence.fromString(text)
        
    except Exception, e:
        print "Error en shortcut", e, text
        return QKeySequence()
    
    return ks

def createAction(parent, caption, 
                 shortcut = None, # QKeySequence
                 name = None,
                 do_i18n = True,
                 checkable = False, 
                 addToParent = True): # Name, 
    '''
    @param parent: Objeto
    @param name: Nombre de la propiedad
    @param caption: Texto de la acción a ser i18nalizdo
    @param shortcut: Texto del atajo a ser i18nalizdo
    '''
    caption = do_i18n and _(caption) or caption
    action = QAction(_(caption), parent)
    if not name:
        name = caption.replace(' ', '')
        name = name.replace('&', '')
        #print name
    actionName = 'action' + name
    action.setObjectName(actionName)
    if shortcut:
        shortcut = do_i18n and _(shortcut) or shortcut 
        sequence = text_to_KeySequence(shortcut)
        action.setShortcut(sequence)
    setattr(parent, actionName, action )
    if checkable:
        action.setCheckable(checkable)
    parent.addAction(action)
    return action

def addActionsToMenu(menu, *action_tuples):
    '''
    Helper for mass menu action creation
    Usage:
    addActionsToMenu(menu,
                     ("&Open", "Ctrl+O", "actionFOpen", {do_i18n = False}),
                     (pos1, pos2, pos3, {x = 2}),
                     None,
                     ()
    )
    '''
    actions = []
    for action_params in action_tuples:
        parent = menu.parent()
        assert parent is not None
        if not action_params:
            menu.addSeparator()
        elif type(action_params) is QMenu:
            menu.addMenu(action_params)
        elif isinstance(action_params, QAction):
            menu.addAction(action_params)
        else:
            kwargs = {}
            if isinstance(action_params[-1], dict):
                largs = action_params[:-1]
                kwargs.update(action_params[-1])
            else:
                largs = action_params
            action = menu.addAction(createAction(parent, *largs, **kwargs))
            actions.append(action)
    return actions
            #action = menu.addAction(createAction(parent, *largs))
#            for key, value in kwargs.iteritems():
#                f = getattr(action, 'set'+key.capitalize(), None)
#                if f:
#                    f(value)

# Key press debugging 
KEY_NAMES = dict([(getattr(QtCore.Qt, keyname), keyname) for keyname in dir(QtCore.Qt) 
                  if keyname.startswith('Key_')])

ANYKEY = -1

def debug_key(key_event):
    ''' Prevents hair loss when debuging what the hell is going on '''
    key = key_event.key()
    mods = []
    print "count: ", key_event.count()
    print "isAutoRepeat: ", key_event.isAutoRepeat()
    print "key: ", key_event.key()
    print "nativeModifiers: ", key_event.nativeModifiers()
    print "nativeScanCode: ", key_event.nativeScanCode()
    print "nativeVirtualKey: ", key_event.nativeVirtualKey()
    print "text: ", unicode(key_event.text()).encode('utf-8')
    print "isAccepted: ", key_event.isAccepted()
    print "modifiers: ", int(key_event.modifiers())
    modifiers = key_event.modifiers()
    if modifiers & QtCore.Qt.AltModifier:
        mods.append("AltModifier")
    if modifiers & QtCore.Qt.ControlModifier:
        mods.append("ControlModifier")
    if modifiers & QtCore.Qt.MetaModifier:
        mods.append("MetaModifier")
    if modifiers & QtCore.Qt.ShiftModifier:
        mods.append("ShiftModifier")
    
    print "%s <%s> Code: %d chr(%d) = %s" % (KEY_NAMES[key],  ", ".join(mods), 
                                              key, key, key < 255 and chr(key) 
                                              or 'N/A')

if __name__ == "__main__":
    print text_to_object_name('Button Text Editor')
    print text_to_object_name('Button Text Editor', 'action')