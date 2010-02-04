#!/usr/bin/env python
#-*- encoding: utf-8 -*-
# Created: 03/02/2010 by defo

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from prymatex.lib.i18n import ugettext as _
import os

def deco(f):
    def wrapped(*largs, **kwargs):
        
        retval = f(*largs, **kwargs)
        print "%s() -> %s" % (f.func_name, retval)
        return retval
    return wrapped 

class PMXTextEdit(QPlainTextEdit):
    _path = ''
    
    def __init__(self, parent, path = ''):
        QTextEdit.__init__(self, parent)
        self.lineNumberArea = LineNumberArea(self)
        
        self.connect(self, SIGNAL("blockCountChanged(int)"), self.updateLineNumberAreaWidth)
        self.connect(self, SIGNAL("updateRequest(const QRect &, int)"), self.updateLineNumberArea)
        self.connect(self, SIGNAL("cursorPositionChanged()"), self.highlightCurrentLine)
        
        self.updateLineNumberAreaWidth(0)
        
        self.highlightCurrentLine()

        #print self.connect(self, SIGNAL("destroyed(QObject)"), self.cleanUp)
        
        self.path = path
        
        
    
    def path(): #@NoSelf
        def fget(self):
            return self._path
        
        def fset(self, value):
            self._path = unicode(value)
            if os.path.exists(value):
                f = open(self.path)
                text = f.read()
                f.close()
                self.setPlainText(text)
                
            elif value: # Si no es nulo
                raise IOError("%s does not exist")
            
        doc = u"Path property QString->unicode/str"
        return locals()
    path = property(**path())
    
       
#    @property
#    def index(self):
#        tabwidget = self.parent()
#        for index in range(tabwidget.count()):
#            widget = tabwidget.widget(index)
#            print widget, self
#            if widget == self:
#                return index
#        return -1
    @property
    def filename(self):
        if self.path:
            return self.path
        return _("This unsaved file")
    
    def getFocus(self):
        self.setFocus(Qt.TabFocusReason)
    
    def setToolTip(self, text):
        tabwidget = self.parent().parent()
        index = tabwidget.indexOf(self)
        tabwidget.setTabToolTip(index, text)
        
    def title(self):
        tabwidget = self.parent().parent()
        #print tabwidget, tabwidget.parent()
        index = tabwidget.indexOf(self)
        return tabwidget.tabText(index)
        
        
    def setTitle(self, text):
        tabwidget = self.parent().parent()
        #print tabwidget, tabwidget.parent()
        index = tabwidget.indexOf(self)
        tabwidget.setTabText(index, text)
    
    def updateTab(self):
        '''
        Updates tab info
        '''
        if self.path:
            self.setTitle(os.path.basename(self.path))
            self.setToolTip(self.path)
        else:
            self.setTitle(_("Unsaved File"))
            self.setToolTip(_("Unsaved File"))
        
    def requestClose(self):
        if self.document().isModified():
            resp = QMessageBox.question(self, _("File modified"), _("%s is modified", self.filename), 
                                 QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
            return resp
        else:
            return True
    
    def afterRemoveEvent(self):
        #print 'afterRemoveEvent', self
        mainwin = self.parent().parent().parent()
        menu = mainwin.window_menu
        menu.windowActionGroup.removeAction(self.menu_action)
        
    def afterInsertionEvent(self):
        #print 'afterRemoveEvent', self
        self.updateTab()
        mainwin = self.parent().parent().parent()
        menu = mainwin.window_menu
        self.menu_action = QAction(self)
        self.connect(self.menu_action, SIGNAL("toggled(bool)"), self.showTab)
        self.menu_action.setText(self.title())
        self.menu_action.setCheckable(True)
        menu.windowActionGroup.addAction(self.menu_action)
    
    def afterModificationEvent(self):
        pass
        
    def showTab(self, checked):
        if checked:
            tw = self.parent().parent()
            index = tw.indexOf(self)
            if index != tw.currentIndex():
                tw.setCurrentIndex(index)
    
    def lineNumberAreaWidth(self):
        digits = 1
        max_cnt = max((1, self.blockCount(),))
        while max_cnt >= 10:
            max_cnt /= 10;
            digits += 1
        space = 3 + self.fontMetrics().width('9') * digits
        #return 30
        return space
    
    
    def updateLineNumberAreaWidth(self, newBlockCount):
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)
    
    def updateLineNumberArea(self, rect, dy):
        if dy:
            self.lineNumberArea.scroll(0, dy);
        else:
            self.lineNumberArea.update(0, rect.y(), self.lineNumberArea.width(), rect.height());
        if (rect.contains(self.viewport().rect())):
            self.updateLineNumberAreaWidth(0)
 
    def resizeEvent(self, e):
        QPlainTextEdit.resizeEvent(self, e)
        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(QRect(cr.left(), cr.top(), 
                                              self.lineNumberAreaWidth(), cr.height()));

    def highlightCurrentLine(self):
        extraSelections = []
        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            lineColor = QColor(Qt.yellow).lighter(180)
            selection.format.setBackground(lineColor);
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extraSelections.append(selection)
        self.setExtraSelections(extraSelections)
        
    
    def lineNumberAreaPaintEvent(self, event):
        
        painter = QPainter(self.lineNumberArea)
        
        painter.fillRect(event.rect(), Qt.lightGray)
        block = self.firstVisibleBlock()
        
        blockNumber = block.blockNumber()
        top = int(self.blockBoundingGeometry(block).translated(self.contentOffset()).top())
        bottom = top + int(self.blockBoundingRect(block).height())

        while block.isValid() and top < event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(blockNumber + 1)
                painter.setPen(Qt.black)
                painter.drawText(0, top, self.lineNumberArea.width(), 
                                      self.fontMetrics().height(),
                                      Qt.AlignRight, number)
            block = block.next()
            top = bottom
            bottom = top + int(self.blockBoundingRect(block).height())
            blockNumber += 1

                
class LineNumberArea(QWidget):
    def __init__(self, editor):
        QWidget.__init__(self, editor)
        
        self.codeEditor = editor
        
    def sizeHint(self):
        
        return QSize(self.codeEditor.lineNumberAreaWidth(), 0)
    
    def paintEvent(self, event):
        self.codeEditor.lineNumberAreaPaintEvent(event)
