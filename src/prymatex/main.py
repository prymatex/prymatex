#!/usr/bin/env python
#-*- encoding: utf-8 -*-
# Created: 01/02/2010 by defo
import os
import sys

def main(argv = sys.argv):
    '''
    GUI entry point
    '''
    #TODO: CLI options
    from prymatex.app import PMXApplication
    app = PMXApplication(argv)
    return app.exec_()

if __name__ == '__main__':
    sys.exit(main())