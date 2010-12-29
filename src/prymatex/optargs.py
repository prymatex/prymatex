# coding: utf-8

'''
Command line parameters
'''
from optparse import OptionParser
import prymatex
#usage, option_list, option_class, version, conflict_handler, description, formatter, add_help_option, prog, epilog)
parser = OptionParser(usage="%prog [options] [files]",
                      description = "Prymatex Text Editor",
                      epilog = "Check project page at %s" % (
                        prymatex.PROJECT_HOME,
                      ))

# Directory where the application should start
parser.add_option('-d', '--startdir', dest='startdir', default = '',
                  help = 'Start directory')

# Configuration file to use
parser.add_option('-c', '--config', dest='config_file',
                  help='Config file'
                  )

# Reverts custom options
parser.add_option('-R', '--reset-config', dest='reste_config', 
                  action= 'store_true',
                  help='Restore default config',
                  default = False
                  )

# A session consists in a set of opened files, thei cursor position and 
# the document layout
parser.add_option('-s', '--session', dest='session_name', 
                  help = 'Open session name')

# Maybe useful for some debugging information
parser.add_option('-D', '--devel', dest='devel', action='store_true', default=False,
                  help = 'Enable developer mode. Useful for plugin developers.')

# Cache should be used by default to store bundle and plugin cache
parser.add_option('-n', '--no-cache', dest='cache', action='store_true', default=False,
                  help=u'Disable Bundle caché')