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

# TODO: Accept Qt Arguments to QtApplication
def runPrymatexApplication(options, files):
    from prymatex.core import app, exceptions
    
    pmx = None
    try:
        pmx = app.PMXApplication()
        
        pmx.buildSettings(options.profile)
        pmx.setupLogging(options.verbose, options.log_pattern)
        
        pmx.replaceSysExceptHook()
        pmx.checkSingleInstance()
        if options.reset_settings:
            pmx.resetSettings()
        pmx.loadGraphicalUserInterface()
        pmx.openArgumentFiles(files)
        return pmx.exec_()
    except exceptions.AlreadyRunningError as ex:
        from PyQt4 import QtGui
        QtGui.QMessageBox.critical(None, ex.title, ex.message, QtGui.QMessageBox.Ok)
    except:
        from traceback import format_exc
        traceback = format_exc()
        print(traceback)
        # Something went very bad tell the user something about the emergency
        #from prymatex.gui.emergency.crashdialog import PMXCrashDialog
        #crashDialog = PMXCrashDialog(traceback)
        #return crashDialog.exec_()
    return -1

def main(args):
    from prymatex.core import cliparser
    options, files = cliparser.parse()
    
    if options.devel:
        from prymatex.utils import autoreload
        autoreload.main(runPrymatexApplication, (options, files))
    else:
        return runPrymatexApplication(options, files)

if __name__ == '__main__':
    sys.exit(main(sys.argv))