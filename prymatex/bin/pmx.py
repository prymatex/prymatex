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

def runPrymatexApplication(profile, args = []):
    from prymatex.core import app, exceptions
    try:
        pmxapp = app.PMXApplication(profile, args)
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
    return pmxapp.exec_()
    
def main(args):
    '''
    GUI entry point.
    '''
    
    from prymatex.optargs import parser
    from prymatex.utils import autoreload
    
    options, args = parser.parse_args(args)
    
    if options.use_reloader:
        autoreload.main(runPrymatexApplication, (options.profile, args))
    else:
        runPrymatexApplication(options.profile, args)

if __name__ == '__main__':
    sys.exit(main(sys.argv))
    