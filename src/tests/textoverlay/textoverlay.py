from PyQt4.Qt import *

class OverlayedQTextEdit(QPlainTextEdit):
    rectStart = None
    rectEnd = None
    
    def __init__(self):
        super(OverlayedQTextEdit, self).__init__()
        self.setWindowTitle("Drag mouse over me")
        self.setPlainText('\n'*10)
    
    def mousePressEvent(self, event):
        super(OverlayedQTextEdit, self).mousePressEvent(event)
        if event.modifiers() == Qt.ControlModifier:
            self.rectStart = event.pos()
            self.cursorStart = self.cursorForPosition(event.pos())
        
    def mouseMoveEvent(self, event):
        if event.modifiers() == Qt.ControlModifier:
            self.rectEnd = event.pos()
            self.cursorEnd = self.cursorForPosition(event.pos())
            self.document().markContentsDirty(self.cursorStart.position(), self.cursorEnd.position())
        else:
            super(OverlayedQTextEdit, self).mouseMoveEvent(event)
        
    def mouseReleaseEvent(self, event):
        super(OverlayedQTextEdit, self).mouseReleaseEvent(event)
        if self.cursorStart != None and self.cursorEnd != None:
            self.document().markContentsDirty(self.cursorStart.position(), self.cursorEnd.position())
            self.rectStart = self.rectEnd = None
            self.cursorStart = self.cursorEnd = None

    
    def paintEvent(self, event):
        retval = super(OverlayedQTextEdit, self).paintEvent(event)
        
        #print self.rectStart, self.rectEnd
        
        if self.rectStart and self.rectEnd:
            painter = QPainter(self.viewport())
            
            pen = QPen("red")
            pen.setWidth(2)
            painter.setPen(pen)
            
            color = QColor()
            color.setAlpha(128)
            painter.setBrush(QBrush(color))
            painter.setOpacity(0.2)
            painter.drawRect(QRect(self.rectStart, self.rectEnd))
            
        return retval

class TestWidget(QWidget):
    def __init__(self):
        super(TestWidget, self).__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel('''
        Palying with overlay
        '''.strip()))
        btn = QPushButton("QWidget")
        btn.pressed.connect(self.showWidget)
        layout.addWidget(btn)
        
        btn = QPushButton("QPlainTextEdit")
        layout.addWidget(btn)
        btn.pressed.connect(self.showTextEdit)
        self.setLayout(layout)
        
    def showWidget(self):
        if not hasattr(self, 'testWidget'):
            self.testWidget = OverlayedTestWidget()
        self.testWidget.show()
    
    def showTextEdit(self):
        if not hasattr(self, 'testTextEdit'):
            self.testTextEdit = OverlayedQTextEdit()
        self.testTextEdit = OverlayedQTextEdit()
        self.testTextEdit.show()
            

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    win = TestWidget()
    
    win.show()
    win.setWindowTitle("Test")
    sys.exit(app.exec_())
    
