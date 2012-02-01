#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import sys

import prymatex

usage="pmx.py [options] [files]"

description = prymatex.__doc__

version = prymatex.get_version(),

epilog = """This program comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome to redistribute
it under certain conditions; for details see LICENSE.txt.
Check project page at %s""" % prymatex.__url__

try:
    import argparse

    new_parser = True

    def _get_parser():
        global usage
        global epilog
        global version
        global description

        parser = argparse.ArgumentParser(usage=usage, 
            description = description,
            version = version,
            epilog = epilog)
        
        parser.add_argument('file', metavar='file', type=unicode,
            nargs='*', help='A file/s to edit', default=[])
        parser.add_argument('-f', '--files', metavar='file', type=unicode,
            nargs='+', help='A file/s to edit', default=[])
        
        # Reverts custom options
        parser.add_argument('--reset-settings', metavar='reste_settings', default = False, 
                            help = 'Restore default settings for selected profile')
        parser.add_argument('-p', '--profile', metavar='profile', default = 'default',
                        help = "Change profile")

        # Maybe useful for some debugging information
        parser.add_argument('--devel', metavar='devel', default=False,
                        help = 'Enable developer mode. Useful for plugin developers.')

        parser.add_argument('--verbose', metavar='verbose', default=0, type=int,
                        help = 'Set verbose level from 0 to 4.')

        return parser

except:
    import optparse

    new_parser = False

    def _resolve_nargs(*opts):
        final_nargs = 1
        for opt in opts:
            nargs = 0
            try:
                start = sys.argv.index(opt) + 1
                for idx, arg in enumerate(sys.argv[start:]):
                    if str(arg).startswith("-"):
                        break
                    nargs += 1
                return nargs
            except ValueError:
                nargs = 1
            if final_nargs < nargs:
                final_nargs = nargs
        return final_nargs

    def _get_parser():
        global usage
        global epilog
        global version
        global description

        parser = optparse.OptionParser(usage=usage, 
            description = description,
            version = version,
            epilog = epilog)
        
        parser.add_option("-f", "--file",
            type="string",
            action="store",
            dest="file",
            default=[],
            help="A file/s to edit",
            nargs=_resolve_nargs("-f", "--file"))
        
        # Reverts custom options
        parser.add_option('--reset-settings', dest='reste_settings', action = 'store_true', default = False, 
                            help = 'Restore default settings for selected profile')
        parser.add_option('-p', '--profile', dest='profile', default = 'default',
                          help = "Change profile")

        # Maybe useful for some debugging information
        parser.add_option('--devel', dest='devel', action='store_true', default=False,
                          help = 'Enable developer mode. Useful for plugin developers.')
        
        parser.add_option('-v', '--verbose', dest='verbose', default=0,
                        help = 'Set verbose level from 0 to 4.')
        
        return parser

def parse():
    filenames = None
    projects_path = None
    extra_plugins = None
    try:
        if new_parser:
            opts = _get_parser().parse_args()
        else:
            opts = _get_parser().parse_args()[0]

        filenames = opts.file \
            if isinstance(opts.file, list) \
            else [opts.file]
        filenames += opts.files \
            if hasattr(opts, 'files') \
            else []
    except Exception, reason:
        print "Args couldn't be parsed."
        print reason
    return opts, filenames
