# coding: utf-8

'''
Command line parameters
'''
from optparse import OptionParser
from prymatex import version

#usage, option_list, option_class, version, conflict_handler, description, formatter, add_help_option, prog, epilog)
parser = OptionParser(usage="%prog [options] [files]",
                      description = version.__doc__,
                      version = version.__version__,
                      epilog = "Check project page at %s" % (
                        version.__url__,
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

parser.add_option('-x', '--no-ipdb', dest="ipdb_excepthook", 
                  action="store_false", help="Disable ipdb stacktrace",
                  default=False)

parser.add_option('-i', '--ipdb', dest="ipdb_excepthook", 
                  action="store_true", help="Enable ipdb stacktrace")


parser.add_option('-p', '--profile', dest='profile',
                  default = 'default',
                  help = "Change profile")

parser.add_option('-P', '--profile-enabled', dest='profile_enabled',
                  action="store_true",
                  default = False,
                  help = "Run profiling for prymatex session")

parser.add_option('-e', '--profile-entries', dest='profile_entries',
                  action="store",
                  type = int, 
                  default = 0,
                  help = "Define profiling entries, assumes -p")