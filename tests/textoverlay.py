import os, sys
sys.path.append(os.path.abspath('..'))

from prymatex.qt import QtCore, QtGui
from prymatex.gui.editor.codehelper import PMXCursorsHelper

class PMXCodeEdit(QtGui.QPlainTextEdit):
    rectStart = None
    rectEnd = None
    
    def __init__(self):
        super(PMXCodeEdit, self).__init__()
        self.cursors = PMXCursorsHelper(self)
    
    @property
    def multiEditMode(self):
        """Retorna si el editor esta en modo multiedit"""
        return self.cursors.hasCursors or self.cursors.isDragCursor
    
    def mousePressEvent(self, event):
        if event.modifiers() == QtCore.Qt.ControlModifier:
            self.cursors.startPoint(event.pos())
        else:
            super(PMXCodeEdit, self).mousePressEvent(event)
        
    def mouseMoveEvent(self, event):
        if event.modifiers() == QtCore.Qt.ControlModifier:
            self.cursors.dragPoint(event.pos())
        else:
            super(PMXCodeEdit, self).mouseReleaseEvent(event)
        
    def mouseReleaseEvent(self, event):
        if event.modifiers() == QtCore.Qt.ControlModifier:
            self.cursors.endPoint(event.pos())
        else:
            super(PMXCodeEdit, self).mouseReleaseEvent(event)

    
    def paintEvent(self, event):
        retval = super(PMXCodeEdit, self).paintEvent(event)
        font_metrics = QtGui.QFontMetrics(self.document().defaultFont())
        
        if self.multiEditMode:
            painter = QtGui.QPainter(self.viewport())
            extraSelections = []
            for cursor in self.cursors:
                if cursor.hasSelection():
                    selection = QtGui.QTextEdit.ExtraSelection()
                    selection.format.setBackground(QtCore.Qt.gray)
                    selection.format.setProperty(QtGui.QTextFormat.FullWidthSelection, True)
                    selection.cursor = cursor
                    extraSelections.append(selection)
                rec = self.cursorRect(cursor)
                cursor = QtCore.QLine(rec.x(), rec.y(), rec.x(), rec.y() + font_metrics.ascent() + font_metrics.descent())
                painter.setPen(QtGui.QPen(QtCore.Qt.blue))
                painter.drawLine(cursor)
            self.setExtraSelections(extraSelections)
            if self.cursors.isDragCursor:
                pen = QtGui.QPen(QtCore.Qt.blue)
                pen.setWidth(2)
                painter.setPen(pen)
                color = QtGui.QColor(QtCore.Qt.yellow)
                color.setAlpha(128)
                painter.setBrush(QtGui.QBrush(color))
                painter.setOpacity(0.2)
                painter.drawRect(self.cursors.getDragCursorRect())
            painter.end()
        return retval

if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    win = PMXCodeEdit()
    
    win.show()
    win.setWindowTitle("Mini Editor")
    sys.exit(app.exec_())
    
