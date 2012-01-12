#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui

from prymatex import resources

class PrymatexStyle(QtGui.QStyle):
    def __init__(self):
        QtGui.QStyle.__init__(self)
        self.icon = resources.getIcon("bundle")
        defaultStyle = QtGui.QApplication.style().objectName()
        self.style = QtGui.QStyleFactory.create(defaultStyle)
    
    def styleHint(self, *args, **kwargs):
        return self.style.styleHint(*args, **kwargs)
    
    def subElementRect(self, *args, **kwargs):
        return self.style.subElementRect(*args, **kwargs)
    
    def pixelMetric(self, *args, **kwargs):
        return self.style.pixelMetric(*args, **kwargs)
        
    def sizeFromContents(self, *args, **kwargs):
        return self.style.sizeFromContents(*args, **kwargs)

    def subControlRect(self, *args, **kwargs):
        return self.style.subControlRect(*args, **kwargs)
    
    def drawPrimitive(self, *args, **kwargs):
        return self.style.drawPrimitive(*args, **kwargs)

    def standardPixmap(self, *args, **kwargs):
        return self.style.standardPixmap(*args, **kwargs)

    def generatedIconPixmap(self, *args, **kwargs):
        return self.style.generatedIconPixmap(*args, **kwargs)
        
    def drawComplexControl(self, *args, **kwargs):
        return self.style.drawComplexControl(*args, **kwargs)

    def hitTestComplexControl(self, *args, **kwargs):
        return self.style.hitTestComplexControl(*args, **kwargs)
    
    def drawControl(self, element, option, painter, widget = 0):
        if (element == QtGui.QStyle.CE_DockWidgetTitle):
            #width of the icon 
            width = self.pixelMetric(QtGui.QStyle.PM_ToolBarIconSize)
            #margin of title from frame 
            margin = self.pixelMetric(QtGui.QStyle.PM_DockWidgetTitleMargin)
            #spacing between icon and title 
            spacing = self.pixelMetric(QtGui.QStyle.PM_LayoutHorizontalSpacing)
          
            point = QtCore.QPoint(margin + option.rect.left(), margin + option.rect.center().y() - width / 2)

            option.rect = option.rect.adjusted(width, 0, 0, 0)
            self.style.drawControl(element, option, painter, widget)
            painter.drawPixmap(point, self.icon.pixmap(width, width))
        else:
            self.style.drawControl(element, option, painter, widget)