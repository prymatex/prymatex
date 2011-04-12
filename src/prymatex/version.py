# -*- coding: utf-8 -*-
# encoding: utf-8
__doc__ = """A PyQt4 based TextMate clone"""

__version_info__ = (0, 0, 1)
__version__ = '.'.join([ str(v) for v in __version_info__])
__url__ = 'http://github.com/D3f0/prymatex'
__author__ = ('Nahuel Defossé',
              'Diego Marcos van Haaster',
              'Pablo Petenello'
              )
__authoremail__ = ( 'nahuel (dto) defosse (at) gmail',
                    'diegomvh (at) gmail',
                    'locurask (at) gmail'
                    )


def show_to_console_version():
    
    print """
    +-------+
    |.....  |   Prymatex %s
    |...    |   
    |...... |   Version: %s
    +-------+.py
    """ % (__doc__, __version__)
    
    
    print "Website: %s" % __url__
    print "Author/s:"
    for author in  __author__:
        print "\t - %s" % author
    
    print "\nFor more information use the -h option"
    