#!/usr/bin/env python
#-*- encoding: utf-8 -*-
# Created: 03/02/2010 by defo
'''
Algunas definciones en Python para simplificar la creación de botones y 
acciones.

'''
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import string
from prymatex.lib.i18n import ugettext as _

to_ascii = lambda s: filter(lambda c: c in string.ascii_letters, s)
to_ascii_cap = lambda s: to_ascii(s).capitalize()
 
def text_to_object_name(text, prefix = None):
    '''
    &Text Button name -> %{prefix}TextButtonName
    '''
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


_available_keys = filter(lambda s: s.startswith('Key_'), dir(Qt))
KEYS_DICT = dict([(name[4:], getattr(Qt, name)) for name in _available_keys])
KEYS_DICT.update({'Ctrl': Qt.CTRL, 'Control': Qt.CTRL, 'CTRL': Qt.CTRL, 
                  'Shift': Qt.SHIFT, 'Shift': Qt.SHIFT,
                  'Alt': Qt.ALT, 'ALT': Qt.ALT,
                  'Meta': Qt.META, 'META': Qt.META,
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


def get_icon(path):
    root = qApp.instace().getThemePath()
    pass



if __name__ == "__main__":
    print text_to_object_name('Button Text Editor')
    print text_to_object_name('Button Text Editor', 'action')