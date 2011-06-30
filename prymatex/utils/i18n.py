'''
Translate strings
'''

from PyQt4 import QtGui
from PyQt4 import QtCore

def ugettext(source, *largs, **kwargs):
    ''' Translate a string '''
    assert isinstance(source, (basestring, QtCore.QString))
    qapp = QtGui.qApp.instance()
    i18n_string = qapp.trUtf8(qapp.tr(source))
    
    if i18n_string.count('%') and largs:
        i18n_string = unicode(i18n_string) % largs
    
    return i18n_string

