#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui

from prymatex import resources

class PrymatexStyle(QtGui.QCommonStyle):
    def __init__(self):
        QtGui.QCommonStyle.__init__(self)
        self.icon = resources.getIcon("bundle")
        self.defaultStyle = QtGui.QStyleFactory.create(QtGui.QApplication.style().objectName())
    
    def combinedLayoutSpacing(self, *args, **kwargs):
        return self.defaultStyle.combinedLayoutSpacing(*args, **kwargs)
    
    def styleHint(self, *args, **kwargs):
        return self.defaultStyle.styleHint(*args, **kwargs)
    
    def subElementRect(self, *args, **kwargs):
        return self.defaultStyle.subElementRect(*args, **kwargs)
    
    def pixelMetric(self, *args, **kwargs):
        return self.defaultStyle.pixelMetric(*args, **kwargs)
        
    def sizeFromContents(self, *args, **kwargs):
        return self.defaultStyle.sizeFromContents(*args, **kwargs)

    def subControlRect(self, *args, **kwargs):
        return self.defaultStyle.subControlRect(*args, **kwargs)

    def standardPixmap(self, *args, **kwargs):
        return self.defaultStyle.standardPixmap(*args, **kwargs)

    def hitTestComplexControl(self, *args, **kwargs):
        return self.defaultStyle.hitTestComplexControl(*args, **kwargs)
    
    def drawItemText(self, *args, **kwargs):
        return self.defaultStyle.drawItemText(*args, **kwargs)
    
    def drawItemPixmap(self, *args, **kwargs):
        return self.defaultStyle.drawItemPixmap(*args, **kwargs)
    
    def drawPrimitive(self, *args, **kwargs):
        return self.defaultStyle.drawPrimitive(*args, **kwargs)
    
    def drawComplexControl(self, *args, **kwargs):
        return self.defaultStyle.drawComplexControl(*args, **kwargs)
    
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
        self.defaultStyle.drawControl(element, option, painter, widget)
    
    def generatedIconPixmap(self, *args, **kwargs):
        return self.defaultStyle.generatedIconPixmap(*args, **kwargs)
    
    def itemPixmapRect(self, *args, **kwargs):
        return self.defaultStyle.itemPixmapRect(*args, **kwargs)
    
    def itemTextRect(self, *args, **kwargs):
        return self.defaultStyle.itemTextRect(*args, **kwargs)
    
    def layoutSpacing(self, *args, **kwargs):
        return self.defaultStyle.layoutSpacing(*args, **kwargs)
    
    def layoutSpacingImplementation(self, *args, **kwargs):
        return self.defaultStyle.layoutSpacingImplementation(*args, **kwargs)

    def polish(self, *args, **kwargs):
        return self.defaultStyle.polish(*args, **kwargs)
    
    def standardIcon(self, *args, **kwargs):
        return self.defaultStyle.standardIcon(*args, **kwargs)
    
    def standardIconImplementation(self, *args, **kwargs):
        return self.defaultStyle.standardIconImplementation(*args, **kwargs)
    
    def standardPalette(self, *args, **kwargs):
        return self.defaultStyle.standardPalette(*args, **kwargs)
    
    def unpolish(self, *args, **kwargs):
        return self.defaultStyle.unpolish(*args, **kwargs)
    