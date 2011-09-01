#!/usr/bin/env python
#-*- encoding: utf-8 -*-

#Setup qt
import sip
sip.setapi('QDate', 2)
sip.setapi('QTime', 2)
sip.setapi('QDateTime', 2)
sip.setapi('QUrl', 2)
sip.setapi('QTextStream', 2)
sip.setapi('QVariant', 2)
sip.setapi('QString', 2)

'''
Misc functions
'''
def amIRunningForzen():
    '''
    @return: True if program is executed in an executable (exe)
    '''
    return globals().has_key('__file__')