#!/usr/bin/env python
#-*- encoding: utf-8 -*-
import os
import sys
    
# this will be replaced at install time
INSTALLED_BASE_DIR = "@ INSTALLED_BASE_DIR @"

if os.path.exists(INSTALLED_BASE_DIR):
    project_basedir = INSTALLED_BASE_DIR
else:
    project_basedir = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(sys.argv[0])))))

if project_basedir not in sys.path:
    sys.path.insert(0, project_basedir)

def main(args):
    '''
    GUI entry point.
    '''
    from prymatex.core import app, exceptions
    from prymatex.optargs import parser
    # TODO: Implement quit and restart
    while True:
        try:
            options, open_args = parser.parse_args(args)
            myapp = app.PMXApplication(open_args, options = options)
        except exceptions.AlreadyRunningError, e:
            return e.RETURN_VALUE
        except Exception, e:
            from traceback import format_exc
            traceback = format_exc()
            # Something went very bad
            # tell the user something about the emergency
            from prymatex.gui.emergency import PMXCrashDialog
            dlg = PMXCrashDialog(traceback)
            dlg.exec_()
        retval = myapp.exec_()
        if retval == 3:
            del myapp
            reload(app)
            continue
        return retval

if __name__ == '__main__':
    sys.exit(main(sys.argv))
    