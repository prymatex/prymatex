from optparse import OptionParser

#usage, option_list, option_class, version, conflict_handler, description, formatter, add_help_option, prog, epilog)
parser = OptionParser(usage="%prog [options] [files]",
                      description = "Prymatex Text Editor",
                      epilog = "A general purpouse text editor")

parser.add_option('-d', '--startdir', dest='startdir',
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
