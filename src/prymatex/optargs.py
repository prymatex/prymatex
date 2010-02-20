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

parser.add_option('-d', '--startdir', dest='startdir', default = '',
                  help = 'Start directory')


parser.add_option('-c', '--config', dest='config_file',
                  help='Config file'
                  )

parser.add_option('-R', '--reset-config', dest='reste_config', 
                  action= 'store_true',
                  help='Restore default config',
                  default = False
                  )

parser.add_option('-s', '--session', dest='session_name', 
                  help = 'Open session name')

parser.add_option('-D', '--devel', dest='devel', action='store_true', default=False,
                  help = 'Enable developer mode. Useful for plugin developers.')

parser.add_option('-n', '--no-cache', dest='cache', action='store_true', default=False,
                  help=u'Disable Bundle caché')