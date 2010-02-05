#!/usr/bin/env python
#-*- encoding: utf-8 -*-
# Created: 05/02/2010 by defo
from PyQt4.Qt import qApp

class CenterWidget(object):
    
    def center(self):
        dsk_geo = qApp.instance().desktop().availableGeometry()
        dwidth, dheight = dsk_geo.width(), dsk_geo.height() 
        width = dwidth * 0.7
        height = dheight * 0.67
        x0 = (dwidth - width) / 2 
        y0 = (dheight - height) / 2
        self.setGeometry(x0,y0,width,height)