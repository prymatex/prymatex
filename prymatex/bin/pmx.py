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

prymatexAppInstance = None

# TODO: Accept Qt Arguments to QtApplication
def runPrymatexApplication(options, files):
    from prymatex.core.app import PMXApplication
    from prymatex.core import exceptions
    
    def runPrymatexInstance(instanceOptions, instanceFiles = []):
        global prymatexAppInstance
        if prymatexAppInstance is not None:
            prymatexAppInstance.unloadGraphicalUserInterface()
            del prymatexAppInstance
        prymatexAppInstance = PMXApplication()
        prymatexAppInstance.buildSettings(instanceOptions.profile)
        prymatexAppInstance.setupLogging(instanceOptions.verbose, instanceOptions.log_pattern)
    
        prymatexAppInstance.replaceSysExceptHook()
        prymatexAppInstance.checkSingleInstance()
        if options.reset_settings:
            prymatexAppInstance.resetSettings()
        prymatexAppInstance.loadGraphicalUserInterface()
        prymatexAppInstance.openArgumentFiles(instanceFiles)
        return prymatexAppInstance.exec_()

    returnCode = -1
    try:
        returnCode = runPrymatexInstance(options, files)
    except exceptions.AlreadyRunningError as ex:
        from PyQt4 import QtGui
        QtGui.QMessageBox.critical(None, ex.title, ex.message, QtGui.QMessageBox.Ok)
    except:
        from traceback import format_exc
        traceback = format_exc()
        print(traceback)

    if returnCode == PMXApplication.RESTART_CODE:
        options.profile = ""
        while returnCode == PMXApplication.RESTART_CODE:
            returnCode = runPrymatexInstance(options)

    return returnCode

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