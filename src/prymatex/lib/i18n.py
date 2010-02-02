

from PyQt4.QtGui import QApplication

def ugettext(string, *largs, **kwargs):
    if not isinstance(string, basestring):
        return string
    
    i18n_string = string
    if i18n_string.count('%') and largs:
        i18n_string = i18n_string % largs
    return i18n_string
    