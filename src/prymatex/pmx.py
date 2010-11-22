#!/usr/bin/env python
#-*- encoding: utf-8 -*-
# Created: 01/02/2010 by defo
'''
    Pryamatex main script.
    Path checking and correcting.
    Instanciate the application and exec_() it :)
'''
import os
import sys
#import logging
#from optparse import OptionParser
basepath = os.path.dirname(__file__)
sys.path.append(os.path.join(basepath, '..'))

def main(argv = sys.argv):
    '''
    GUI entry point.
    '''
  
    from prymatex import app
    from prymatex.lib import exceptions
    # TODO: Implement quit and restart
    while True:
        try:
            myapp = app.PMXApplication(argv)
            #myapp.logger = logger 
        except exceptions.AlreadyRunningError, e:
            return e.RETURN_VALUE
        retval = myapp.exec_()
        if retval == 3:
            del myapp
            reload(app)
            reload(exceptions)
            continue
        return retval

if __name__ == '__main__':
    # create logger with "spam_application"
    sys.exit(main())

