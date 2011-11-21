#!/usr/bin/env python
#-*- encoding: utf-8 -*-
import os
import sys
try:
    import psyco
    print "Psyco accel found"
except ImportError, e:
    pass

    
# this will be replaced at install time
INSTALLED_BASE_DIR = "@ INSTALLED_BASE_DIR @"

if os.path.exists(INSTALLED_BASE_DIR):
    project_basedir = INSTALLED_BASE_DIR
else:
    project_basedir = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(sys.argv[0])))))

if project_basedir not in sys.path:
    sys.path.insert(0, project_basedir)

def parseArguments(args):
    import prymatex
    from optparse import OptionParser
    #usage, option_list, option_class, version, conflict_handler, description, formatter, add_help_option, prog, epilog)
    parser = OptionParser(usage="%prog [options] [files]", description = prymatex.__doc__, version = prymatex.get_version(),
                          epilog = "Check project page at %s" % prymatex.__url__)

    # Reverts custom options
    parser.add_option('--reset-settings', dest='reste_settings', action = 'store_true', default = False, 
                        help = 'Restore default settings for selected profile')
    parser.add_option('-p', '--profile', dest='profile', default = 'default',
                      help = "Change profile")

    # Maybe useful for some debugging information
    parser.add_option('--devel', dest='devel', action='store_true', default=False,
                      help = 'Enable developer mode. Useful for plugin developers.')

    options, args = parser.parse_args(args)
    #parser.error("options --alert and --menu are mutually exclusive")
    return options, args
    
def runPrymatexApplication(options, args):
    from prymatex.core import app, exceptions
    try:
        pmx = app.PMXApplication(options.profile, args)
        pmx.replaceSysExceptHook()
        pmx.checkSingleInstance()
        if options.reste_settings:
            pmx.resetSettings()
    except exceptions.AlreadyRunningError, ex:
        from PyQt4 import QtGui
        QtGui.QMessageBox.critical(None, ex.title, ex.message, QtGui.QMessageBox.Ok)
        return -1
    except:
        from traceback import format_exc
        traceback = format_exc()
        # Something went very bad tell the user something about the emergency
        from prymatex.gui.emergency.crashdialog import PMXCrashDialog
        dlg = PMXCrashDialog(traceback)
        dlg.exec_()
    return pmx.exec_()    
    
def main(args):
    options, args = parseArguments(args)
    
    if options.devel:
        from prymatex.utils import autoreload
        autoreload.main(runPrymatexApplication, (options, args))
    else:
        runPrymatexApplication(options, args)

if __name__ == '__main__':
    sys.exit(main(sys.argv))
