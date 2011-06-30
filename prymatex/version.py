# -*- coding: utf-8 -*-
# encoding: utf-8
__doc__ = """A PyQt4 based TextMate clone"""

__version_info__ = (0, 0, 1)
__version__ = '.'.join([ str(v) for v in __version_info__])
__url__ = 'http://prymatex.org'
__author__ = ('Nahuel Defossé',
              'Diego Marcos van Haaster',
              'Pablo Petenello'
              )
__authoremail__ = ( 'nahuel (dto) defosse (at) gmail',
                    'diegomvh (at) gmail',
                    'locurask (at) gmail'
                    )


    
__extra_version_string__ = ("""
+-------+
|.....  |   Prymatex %(doc)s
|...    |   
|...... |   Version: %(version)s
+-------+.py

Website: %(website)s
Author/s:
%(authors)s

For more information use the -h option
""" % dict(doc = __doc__, version = __version__,
           website = __url__, 
           authors = '\n'.join(['\t%s' % a for a in __author__]),
           )).strip()

