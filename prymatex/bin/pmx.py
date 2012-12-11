#!/usr/bin/env python
#-*- encoding: utf-8 -*-
import os
import sys
import importlib


# this will be replaced at install time
INSTALLED_BASE_DIR = "@ INSTALLED_BASE_DIR @"

if os.path.exists(INSTALLED_BASE_DIR):
    project_basedir = INSTALLED_BASE_DIR
else:
    project_basedir = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(sys.argv[0])))))

if project_basedir not in sys.path:
    sys.path.insert(0, project_basedir)

prymatexAppInstance = None

#===============================================================================
# Note PyQt4 is needed by core so basic exceptions wont be even raised
#===============================================================================
BASIC_IMPORTS = ('sip', 'PyQt4', 'zmq')
def areBasicImportsAvaliable():
    '''
    @return: True if all basic imports are available
    '''
    try:
        for name in BASIC_IMPORTS:
            importlib.import_module(name)
    except ImportError:
        return False
    return True


# TODO: Accept Qt Arguments to QtApplication
def runPrymatexApplication(options, files):
    from prymatex.core.app import PMXApplication
    from prymatex.core import exceptions

    def runPrymatexInstance(instanceOptions, instanceFiles=[]):
        global prymatexAppInstance
        if prymatexAppInstance is not None:
            prymatexAppInstance.unloadGraphicalUserInterface()
            del prymatexAppInstance
        prymatexAppInstance = PMXApplication()
        try:
            prymatexAppInstance.buildSettings(instanceOptions.profile)
        except ValueError:
            return
        prymatexAppInstance.setupLogging(instanceOptions.verbose, instanceOptions.log_pattern)
        prymatexAppInstance.options = instanceOptions
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
    except exceptions.EnviromentNotSuitable:
        print "Prymatex can't run. Basic imports can't be found. Running in virtualenv?"


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
    if not areBasicImportsAvaliable():
        print
        print "Prymatex can't be started. Basic imports are note available."
        print "Check if you have: %s" % ', '.join(BASIC_IMPORTS)
        print
        return

    from prymatex.core import cliparser
    options, files = cliparser.parse()

    if options.devel:
        from prymatex.utils import autoreload
        autoreload.main(runPrymatexApplication, (options, files))
    else:
        return runPrymatexApplication(options, files)

if __name__ == '__main__':
    sys.exit(main(sys.argv))
