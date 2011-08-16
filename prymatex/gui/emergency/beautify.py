'''
Colorize text
'''

__all__ = ['beautifyTraceback', ]

from prymatex.core import amIRunningForzen

_pygmentsAvailable = False
if not amIRunningForzen():
    try:
        from pygments import highlight
        from pygments.lexers import PythonLexer
        from pygments.formatters import HtmlFormatter
        _pygmentsAvailable = True
    except ImportError:
        pass # _pygmentsAvailable = False

def beautifyTraceback(tracebackText):
    # Should I check with globals().has_key('highlight') ?
    if _pygmentsAvailable:
        tracebackText = highlight(tracebackText, 
                                  PythonLexer(), 
                                  HtmlFormatter(noclasses = True))
    return tracebackText