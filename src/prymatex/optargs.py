# coding: utf-8

'''
Command line parameters
'''
from optparse import OptionParser
from prymatex import version

#usage, option_list, option_class, version, conflict_handler, description, formatter, add_help_option, prog, epilog)
parser = OptionParser(usage="%prog [options] [files]",
                      description = version.__doc__,
                      #version = version.__version__,
                      version = version.__extra_version_string__,
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

parser.add_option('-P', '--profiling', dest='profiling',
                  action="store_true",
                  default = False,
                  help = "Run profiling for prymatex session")

parser.add_option('-e', '--profiling-entries', dest='profiling_entries',
                  action="store",
                  type = int, 
                  default = 0,
                  help = "Define profiling entries, assumes -p")

parser.add_option('-N', '--no-bundles', dest='no_bundles',action="store_true", default=False, help="Do not load bundles")

# TODO: Check if any of these options are valuables for the parser
'''
-nograb, tells Qt that it must never grab the mouse or the keyboard.
-dograb (only under X11), running under a debugger can cause an implicit -nograb, use -dograb to override.
-sync (only under X11), switches to synchronous mode for debugging.
See Debugging Techniques for a more detailed explanation.
All Qt programs automatically support the following command line options:
-style= style, sets the application GUI style. Possible values are motif, windows, and platinum. If you compiled Qt with additional styles or have additional styles as plugins these will be available to the -style command line option.
-style style, is the same as listed above.
-stylesheet= stylesheet, sets the application styleSheet. The value must be a path to a file that contains the Style Sheet. Note: Relative URLs in the Style Sheet file are relative to the Style Sheet file's path.
-stylesheet stylesheet, is the same as listed above.
-session= session, restores the application from an earlier session.
-session session, is the same as listed above.
-widgetcount, prints debug message at the end about number of widgets left undestroyed and maximum number of widgets existed at the same time
-reverse, sets the application's layout direction to Qt::RightToLeft
-graphicssystem, sets the backend to be used for on-screen widgets and QPixmaps. Available options are raster and opengl.
The X11 version of Qt supports some traditional X11 command line options:
-display display, sets the X display (default is $DISPLAY).
-geometry geometry, sets the client geometry of the first window that is shown.
-fn or -font font, defines the application font. The font should be specified using an X logical font description. Note that this option is ignored when Qt is built with fontconfig support enabled.
-bg or -background color, sets the default background color and an application palette (light and dark shades are calculated).
-fg or -foreground color, sets the default foreground color.
-btn or -button color, sets the default button color.
-name name, sets the application name.
-title title, sets the application title.
-visual TrueColor, forces the application to use a TrueColor visual on an 8-bit display.
-ncols count, limits the number of colors allocated in the color cube on an 8-bit display, if the application is using the QApplication::ManyColor color specification. If count is 216 then a 6x6x6 color cube is used (i.e. 6 levels of red, 6 of green, and 6 of blue); for other values, a cube approximately proportional to a 2x3x1 cube is used.
-cmap, causes the application to install a private color map on an 8-bit display.
-im, sets the input method server (equivalent to setting the XMODIFIERS environment variable)
-inputstyle, defines how the input is inserted into the given widget, e.g., onTheSpot makes the input appear directly in the widget, while overTheSpot makes the input appear in a box floating over the widget and is not inserted until the editing is done.
S
'''
