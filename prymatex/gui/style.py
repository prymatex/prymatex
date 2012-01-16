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
    
    def combinedLayoutSpacing(self, *args, **kwargs):
        return self.style.combinedLayoutSpacing(*args, **kwargs)
    
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

    def standardPixmap(self, *args, **kwargs):
        return self.style.standardPixmap(*args, **kwargs)

    def hitTestComplexControl(self, *args, **kwargs):
        return self.style.hitTestComplexControl(*args, **kwargs)
    
    def drawItemText(self, *args, **kwargs):
        return self.style.drawItemText(*args, **kwargs)
    
    def drawItemPixmap(self, *args, **kwargs):
        return self.style.drawItemPixmap(*args, **kwargs)
    
    def drawPrimitive(self, *args, **kwargs):
        return self.style.drawPrimitive(*args, **kwargs)
    
    def drawComplexControl(self, *args, **kwargs):
        return self.style.drawComplexControl(*args, **kwargs)
    
    def drawControl(self, element, option, painter, widget):
        if (element == QtGui.QStyle.CE_DockWidgetTitle):
            #width of the icon 
            width = self.pixelMetric(QtGui.QStyle.PM_ToolBarIconSize)
            #margin of title from frame 
            margin = self.pixelMetric(QtGui.QStyle.PM_DockWidgetTitleMargin)
            #spacing between icon and title 
            spacing = self.pixelMetric(QtGui.QStyle.PM_LayoutHorizontalSpacing)
          
            point = QtCore.QPoint(margin + option.rect.left(), margin + option.rect.center().y() - width / 2)
            
            painter.drawPixmap(point, self.icon.pixmap(width, width))
            option.rect = option.rect.adjusted(width, 0, 0, 0)
        self.style.drawControl(element, option, painter, widget)
    
    def generatedIconPixmap(self, *args, **kwargs):
        return self.style.generatedIconPixmap(*args, **kwargs)
    
    def itemPixmapRect(self, *args, **kwargs):
        return self.style.itemPixmapRect(*args, **kwargs)
    
    def itemTextRect(self, *args, **kwargs):
        return self.style.itemTextRect(*args, **kwargs)
    
    def layoutSpacing(self, *args, **kwargs):
        return self.style.layoutSpacing(*args, **kwargs)
    
    def layoutSpacingImplementation(self, *args, **kwargs):
        return self.style.layoutSpacingImplementation(*args, **kwargs)

    def polish(self, *args, **kwargs):
        return self.style.polish(*args, **kwargs)
    
    def standardIcon(self, *args, **kwargs):
        return self.style.standardIcon(*args, **kwargs)
    
    def standardIconImplementation(self, *args, **kwargs):
        return self.style.standardIconImplementation(*args, **kwargs)
    
    def standardPalette(self, *args, **kwargs):
        return self.style.standardPalette(*args, **kwargs)
    
    def unpolish(self, *args, **kwargs):
        return self.style.unpolish(*args, **kwargs)
    