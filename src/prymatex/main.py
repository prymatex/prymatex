#!/usr/bin/env python
#-*- encoding: utf-8 -*-
# Created: 01/02/2010 by defo
import os
import sys
sys.path.append('..')

def main(argv = sys.argv):
    '''
    GUI entry point
    '''
    from prymatex import app
    from prymatex.lib import exceptions
    try:
        myapp = app.PMXApplication(argv)
    except exceptions.AlreadyRunningError, e:
        return e.RETURN_VALUE
         
    return myapp.exec_()

if __name__ == '__main__':
    sys.exit(main())