#!/usr/bin/env python
#-*- encoding: utf-8 -*-
# Created: 01/02/2010 by defo
'''
    Pryamatex main script.
    Path checking and correcting.
    Instanciate the application and exec_() it :)
'''
import os
import sys
from traceback import format_exc

PRYMATEX_BASEPATH = os.path.dirname(__file__)
sys.path.append(os.path.join(PRYMATEX_BASEPATH, '..'))

def main(args):
    '''
    GUI entry point.
    '''
    from prymatex.core import app
    from prymatex.lib import exceptions
            
    # TODO: Implement quit and restart
    while True:
        try:
            myapp = app.PMXApplication(args[1:])
            #myapp.logger = logger 
        except exceptions.AlreadyRunningError, e:
            return e.RETURN_VALUE
        except Exception, e:
            traceback = format_exc()
            
            # Something went very bad
            # tell the user something about the emergency
            from prymatex.gui.emergency import PMXCrashDialog
            #from PyQt4.QtGui import qApp
            #myapp = PMXEmergencyApplication()
            dlg = PMXCrashDialog(traceback_text=traceback)
            #dlg.exec_()
            #qApp.exec_()
            #raise e
            #from PyQt4.QtGui import QDialog
            #dlg = QDialog()
            dlg.exec_()
            
            raise e
        retval = myapp.exec_()
        if retval == 3:
            del myapp
            reload(app)
            reload(exceptions)
            continue
        return retval

if __name__ == '__main__':
    # create logger with "spam_application"
    sys.exit(main(sys.argv))

