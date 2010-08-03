from PyQt4.QtGui import QWidget, QPainter
from PyQt4.QtCore import Qt, QSize

class PMXSideArea(QWidget):
    def __init__(self, editor):
        super(PMXSideArea, self).__init__(editor)
        self.editor = editor
    
    def sizeHint(self):
        return QSize(self.editor.lineNumberAreaWidth(), 0)
    
    def paintEvent(self, event):
        self.lineNumberAreaPaintEvent(event)
    
    def lineNumberAreaPaintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(event.rect(), Qt.white)
        
        block = self.editor.firstVisibleBlock()
        current_block = self.editor.document().findBlock(self.editor.textCursor().position())
        
        blockNumber = block.blockNumber()
        top = int(self.editor.blockBoundingGeometry(block).translated(self.editor.contentOffset()).top())
        bottom = top + int(self.editor.blockBoundingRect(block).height())

        while block.isValid() and top < event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(blockNumber + 1)
                painter.setPen(Qt.lightGray)
                font = painter.font()
                font.setBold(block == current_block)
                painter.setFont(font)
                painter.drawText(-7, top, self.width(), self.fontMetrics().height(), Qt.AlignRight, number)
                    
            block = block.next()
            top = bottom
            bottom = top + int(self.editor.blockBoundingRect(block).height())
            blockNumber += 1
            
        painter.end()
        super(PMXSideArea, self).paintEvent(event)