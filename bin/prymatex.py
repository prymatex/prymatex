#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import sys
import os
import importlib
import argparse

# this will be replaced at install time
INSTALLED_BASE_DIR = "@ INSTALLED_BASE_DIR @"

if os.path.exists(INSTALLED_BASE_DIR):
    project_basedir = INSTALLED_BASE_DIR
else:
    project_basedir = os.path.abspath(
        os.path.dirname(os.path.dirname(os.path.realpath(sys.argv[0])))
    )

if project_basedir not in sys.path:
    sys.path.insert(0, project_basedir)

import prymatex

prymatexAppInstance = None

# ----------------------- BUILD PRYMATEX INSTANCE AND RUN
def runPrymatexApplication(options, files):
    from prymatex.core.app import PrymatexApplication
    from prymatex.core import exceptions
    
    def runPrymatexInstance(instanceOptions, instanceFiles=[]):
        global prymatexAppInstance
        if prymatexAppInstance is not None:
            prymatexAppInstance.unloadGraphicalUserInterface()
            del prymatexAppInstance
        prymatexAppInstance = PrymatexApplication.instance(instanceOptions, argv = sys.argv)
        prymatexAppInstance.checkSingleInstance()
        prymatexAppInstance.loadGraphicalUserInterface()
        # ---- Open files
        for path in files:
            prymatexAppInstance.openPath(path)
        return prymatexAppInstance.execute()

    returnCode = PrymatexApplication.RESTART_CODE
    try:
        while returnCode == PrymatexApplication.RESTART_CODE:
            returnCode = runPrymatexInstance(options, files)
            # Clean in case of restart
            options.profile, files = "", []
    except exceptions.EnviromentNotSuitable as ex:
        print(ex)
        returnCode = -1

    except exceptions.AlreadyRunningError as ex:
        print(ex)
        returnCode = -2
    except:
        from traceback import format_exc
        traceback = format_exc()
        print(traceback)
        returnCode = -3

    return returnCode

# ----------------------- CLI PARSER
cliParser = argparse.ArgumentParser(
    usage="%(prog)s [options] [files]",
    description=prymatex.__doc__,
    epilog="""This program comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome to redistribute
it under certain conditions; for details see LICENSE.txt.
Check project page at %s""" % prymatex.__url__
)

cliParser.add_argument('file', metavar='file', type=str,
    nargs='*', help='A file/s to edit', default=[])
cliParser.add_argument('-f', '--files', metavar='file', type=str,
    nargs='+', help='A file/s to edit', default=[])

# Reverts custom options
cliParser.add_argument('--reset-settings', action='store_true', default=False,
                    help='Restore default settings for selected profile')

cliParser.add_argument('-p', '--profile', metavar='profile', nargs="?", default="",
                help="Change profile")

# Maybe useful for some debugging information
cliParser.add_argument('-d', '--devel', default=False, action='store_true',
                help='Enable developer mode. Useful for plugin developers.')

cliParser.add_argument('--verbose', default=2, type=int,
                help='Set verbose level from 0 to 4.')

cliParser.add_argument('--log-pattern', default='', type=str,
                help='Set filter pattern for logging')

cliParser.add_argument('-n', '--no-splash', default=False, action='store_true',
                    help='Show spalsh screen')

cliParser.add_argument('--version', action='version', version='%%(prog)s %s' % prymatex.get_version())

def cliparser():
    filenames = None
    projects_path = None
    extra_plugins = None
    try:
        opts = cliParser.parse_args()
        filenames = opts.file \
            if isinstance(opts.file, list) \
            else [opts.file]
        filenames += opts.files \
            if hasattr(opts, 'files') \
            else []
    except Exception as reason:
        print("Arguments couldn't be parsed.")
        print(reason)
    return opts, filenames

def main(args):
    options, files = cliparser()

    if options.devel:
        from prymatex.utils import autoreload
        autoreload.main(runPrymatexApplication, (options, files))
    else:
        return runPrymatexApplication(options, files)

if __name__ == '__main__':
    sys.exit(main(sys.argv))
