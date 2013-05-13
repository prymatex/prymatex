import sys
import asyncore
import socket
from PyQt4 import QtCore, QtGui

class EchoHandler(asyncore.dispatcher_with_send):
    def handle_read(self):
        data = self.recv(8192)
        if data:
            self.send(data)

class EchoServer(asyncore.dispatcher):
    def __init__(self, host, port, qtThread):
        asyncore.dispatcher.__init__(self)
        self.qtThread = qtThread
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)

    def handle_accept(self):
        pair = self.accept()
        if pair is None:
            pass
        else:
            sock, addr = pair
            self.qtThread.incomingConnection.emit('Incoming connection from %s' % repr(addr))
            handler = EchoHandler(sock)

class CustomThread(QtCore.QThread):
    incomingConnection = QtCore.pyqtSignal(str)
    def __init__(self, parent = None):
        QtCore.QObject.__init__(self)
        server = EchoServer('localhost', 8080, self)
        
    def run(self):
        asyncore.loop()

class SomeQtWidget(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.text = QtGui.QPlainTextEdit(self)
        self.text.resize(self.size())
        self.thread = CustomThread()
        self.thread.incomingConnection.connect(self.on_incomingConnection)
        self.thread.start()
    
    def on_incomingConnection(self, cadena):
        cursor = self.text.textCursor()
        cursor.insertText(cadena)

    def log(self, text):
        self.text.appendPlainText(":%s" % str(text))

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = SomeQtWidget()
    window.show()
    sys.exit(app.exec_())
