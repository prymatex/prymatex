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
        self.highest_line = 0
        self.bookmarkArea = 12
        self.foldArea = 12
        self.foreground = None 
        self.background = None 
        
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

            # Draw the line number right justified at the y position of the
            # line. 3 is a magic padding number. drawText(x, y, text).
            if block.isVisible():
                painter.drawText(self.width() - self.foldArea - font_metrics.width(str(line_count)) - 3,
                    round(position.y()) + font_metrics.ascent() + font_metrics.descent() - 1,
                    str(line_count))

                #Bookmarks
                if block in self.editor.bookmarks:
                    painter.drawPixmap(1,
                        round(position.y()) + font_metrics.ascent() + font_metrics.descent() - resources.IMAGES["bookmarkflag"].height(),
                        resources.IMAGES["bookmarkflag"])

                userData = block.userData()

                #Folding
                mark = self.editor.folding.getFoldingMark(block)
                if self.editor.folding.isStart(mark):
                    if userData.folded:
                        painter.drawPixmap(self.width() - resources.IMAGES["foldingcollapsed"].width() - 1,
                            round(position.y()) + font_metrics.ascent() + font_metrics.descent() - resources.IMAGES["foldingcollapsed"].height(),
                            resources.IMAGES["foldingcollapsed"])
                    else:
                        painter.drawPixmap(self.width() - resources.IMAGES["foldingtop"].width() - 1,
                            round(position.y()) + font_metrics.ascent() + font_metrics.descent() - resources.IMAGES["foldingtop"].height(),
                            resources.IMAGES["foldingtop"])
                elif self.editor.folding.isStop(mark):
                    painter.drawPixmap(self.width() - resources.IMAGES["foldingcollapsed"].width() - 1,
                        round(position.y()) + font_metrics.ascent() + font_metrics.descent() - resources.IMAGES["foldingcollapsed"].height(),
                        resources.IMAGES["foldingbottom"])
            
            block = block.next()

        self.highest_line = line_count

        painter.end()
        QtGui.QWidget.paintEvent(self, event)

    def mousePressEvent(self, event):
        xofs = self.width() - self.foldArea
        xobs = self.bookmarkArea
        font_metrics = QFontMetrics(self.editor.document().defaultFont())
        fh = font_metrics.lineSpacing()
        ys = event.posF().y()
        lineNumber = 0

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
            if event.pos().x() > xofs:
                if block.userData().folded:
                    self.editor.codeFoldingUnfold(block)
                else:
                    self.editor.codeFoldingFold(block)
            else:
                self.editor.toggleBookmark(block)