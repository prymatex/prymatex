#!/usr/bin/env python
#-*- encoding: utf-8 -*-
# Created: 01/02/2010 by defo
import os
import sys
import logging

basepath = os.path.dirname(__file__)
sys.path.append(os.path.join(basepath, '..'))

def main(argv = sys.argv):
    '''
    GUI entry point
    '''
    from prymatex import app
    from prymatex.lib import exceptions
    while True:
        
        try:
            myapp = app.PMXApplication(argv)
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
    logger = logging.getLogger("")
    logger.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    fh = logging.FileHandler("messages.log")
    fh.setLevel(logging.DEBUG)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    # create formatter and add it to the handlers
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)
    logger.info("Application startup")
    sys.exit(main())

