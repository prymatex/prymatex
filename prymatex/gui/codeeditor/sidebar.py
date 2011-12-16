#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QPixmap, QFontMetrics
from PyQt4.Qt import QColor, QSize
from prymatex.gui.codeeditor.userdata import PMXBlockUserData
from prymatex import resources

#based on: http://john.nachtimwald.com/2009/08/15/qtextedit-with-line-numbers/ (MIT license)
class PMXSidebar(QtGui.QWidget):
    def __init__(self, editor):
        super(PMXSidebar, self).__init__(editor)
        self.editor = editor
        self.showBookmarks = True
        self.showLineNumbers = True
        self.showFolding = False
        self.bookmarkArea = 12
        self.foldArea = 12
        self.foreground = None
        self.background = None
        self.images = {}
        for key in ["bookmarkflag", "foldingcollapsed", "foldingtop", "foldingbottom"]:
            self.images[key] = resources.getImage(key)

    @property
    def padding(self):
        if self.showLineNumbers or self.showFolding or self.showBookmarks:
            return 10
        return 0
        
    def sizeHint(self):
        return QtGui.QSize(self.editor.lineNumberAreaWidth(), 0)

    def paintEvent(self, event):
        page_bottom = self.editor.viewport().height()
        font_metrics = QFontMetrics(self.editor.document().defaultFont())
        current_block = self.editor.document().findBlock(self.editor.textCursor().position())

        painter = QtGui.QPainter(self)
        painter.fillRect(self.rect(), self.background)

        block = self.editor.firstVisibleBlock()
        viewport_offset = self.editor.contentOffset()
        line_count = block.blockNumber()
        painter.setPen(self.foreground)
        while block.isValid():
            line_count += 1
            # The top left position of the block in the document
            position = self.editor.blockBoundingGeometry(block).topLeft() + viewport_offset
            # Check if the position of the block is out side of the visible area
            if position.y() > page_bottom:
                break

            font = painter.font()
            font.setBold(block == current_block)
            painter.setFont(font)

            # Draw the line number right justified at the y position of the line.
            if block.isVisible():
                #Line Numbers
                if self.showLineNumbers:
                    leftPosition = self.width() - font_metrics.width(str(line_count)) - 2
                    if self.showFolding:
                        leftPosition -= self.foldArea
                    painter.drawText(leftPosition,
                        round(position.y()) + font_metrics.ascent() + font_metrics.descent() - 1,
                        str(line_count))

                #Bookmarks
                if self.showBookmarks and block in self.editor.bookmarks:
                    painter.drawPixmap(2,
                        round(position.y()) + font_metrics.ascent() + font_metrics.descent() - self.images["bookmarkflag"].height(),
                        self.images["bookmarkflag"])
                
                #Folding
                if self.showFolding:
                    userData = block.userData()
    
                    mark = self.editor.folding.getFoldingMark(block)
                    if self.editor.folding.isStart(mark):
                        if userData.folded:
                            painter.drawPixmap(self.width() - self.images["foldingcollapsed"].width() - 1,
                                round(position.y()) + font_metrics.ascent() + font_metrics.descent() - self.images["foldingcollapsed"].height(),
                                self.images["foldingcollapsed"])
                        else:
                            painter.drawPixmap(self.width() - self.images["foldingtop"].width() - 1,
                                round(position.y()) + font_metrics.ascent() + font_metrics.descent() - self.images["foldingtop"].height(),
                                self.images["foldingtop"])
                    elif self.editor.folding.isStop(mark):
                        painter.drawPixmap(self.width() - self.images["foldingcollapsed"].width() - 1,
                            round(position.y()) + font_metrics.ascent() + font_metrics.descent() - self.images["foldingcollapsed"].height(),
                            self.images["foldingbottom"])
            
            block = block.next()

        painter.end()
        QtGui.QWidget.paintEvent(self, event)

    def mousePressEvent(self, event):
        xofs = self.width() - self.foldArea
        xobs = self.bookmarkArea
        font_metrics = QFontMetrics(self.editor.document().defaultFont())
        fh = font_metrics.lineSpacing()
        ys = event.posF().y()
        
        if event.pos().x() > xofs or event.pos().x() < xobs:
            block = self.editor.firstVisibleBlock()
            viewport_offset = self.editor.contentOffset()
            page_bottom = self.editor.viewport().height()
            while block.isValid():
                position = self.editor.blockBoundingGeometry(block).topLeft() + viewport_offset
                if position.y() > page_bottom:
                    break
                if position.y() < ys and (position.y() + fh) > ys:
                    break
                block = block.next()
            if event.pos().x() > xofs and self.editor.folding.isFoldingMark(block):
                if block.userData().folded:
                    self.editor.codeFoldingUnfold(block)
                else:
                    self.editor.codeFoldingFold(block)
            else:
                self.editor.toggleBookmark(block)