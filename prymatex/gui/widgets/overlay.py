from PyQt4 import QtCore, QtGui
import re



class PMXMessageOverlay(object):
    messageFadedOut = QtCore.pyqtSignal()
    messageFadedIn = QtCore.pyqtSignal()
    ''' 
    Mixin for displaying overlayed messages in a QWidget instance.
    Please note that you should:
        * Use the mixin on toplevel elements (no QWidgets, but QPlainTextEdit, QWebView, etc.)
        * You should call updateMessagePosition at least in resizeEvent of your subclass 
    '''
    def __init__(self):
        # Signals
        self.messageOverlay = LabelOverlayWidget(text = "", parent = self)
        self.messageOverlay.fadedIn.connect(self.messageFadedIn)
        self.messageOverlay.fadedOut.connect(self.messageFadedOut)
        self.messageOverlay.messageClicked.connect(self.messageClicked)
        self.messageOverlay.linkActivated.connect(self.messageLinkActivated)
        
    def messageFadedIn(self):
        ''' Override '''
        #print "Message appeared"
        pass
    
    def messageFadedOut(self):
        ''' Override '''
        #print "Message disappeared"
        pass
    
    def messageLinkActivated(self, link):
        ''' Override '''
        pass
    
    def showMessage(self, message, timeout = None, icon = None, pos = None ):
        self.messageOverlay.setText(message)
        self.messageOverlay.updatePosition()
        self.messageOverlay.adjustSize()
        if unicode(message):
            self.messageOverlay.fadeIn()
        else:
            self.messageOverlay.fadeOut()
            
    def clarMessage(self):
        self.messageOverlay.fadeOut()
    
    def messageClicked(self):
        self.clarMessage()       
        
    def updateMessagePosition(self):
        self.messageOverlay.updatePosition()

        
        
class LabelOverlayWidget(QtGui.QLabel):
    ''' 
    Inner message QLabel.
    StyleSheet
    Don't use this widget separately, please use PMXMessageOverlay API
    '''
    fadedOut = QtCore.pyqtSignal()
    fadedIn = QtCore.pyqtSignal()
    messageClicked = QtCore.pyqtSignal()
    
    
    STYLESHEET = '''
    QLabel, QLabel link {
        color: rgb(0, 0, 0);
        background-color: rgb(248, 240, 200);
        border: 1px solid;
        border-color: rgb(173, 114, 47);
        border-radius: 5px;
        padding: 2px;
    }
    '''
    
    def __init__(self, text="", parent=None):
        super(LabelOverlayWidget, self).__init__(text, parent)
        self.paddingLeft = 10
        self.paddingBottom = 10
        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(32)
        self.timer.timeout.connect(self.updateOpacity)
        self.speed = 0
        self.setStyleSheet(self.STYLESHEET)
        self.opacity = 0
    
    
    def setParent(self, parent):
        self.updatePosition()
        return super(LabelOverlayWidget, self).setParent(parent)
  
    def updatePosition(self):
        
        if hasattr(self.parent(), 'viewport'):
            parentRect = self.parent().viewport().rect()
        else:
            parentRect = self.parent().rect()
            
        if not parentRect:
            return
            
        x = parentRect.width() - self.width() - self.paddingLeft
        y = parentRect.height() - self.height() - self.paddingBottom
        self.setGeometry(x, y, self.width(), self.height())
        
        
    
    def resizeEvent(self, event):
        super(LabelOverlayWidget, self).resizeEvent(event)
        self.updatePosition()
    
    def showEvent(self, event):
        self.updatePosition()
        return super(LabelOverlayWidget, self).showEvent(event)
  
    def enterEvent(self, event):
        """ Mouse hovered the messge """
        pass
    
    FULL_THERSHOLD = 0.7
    DEFAULT_FADE_SPEED = 0.15
    
    def fadeIn(self, force = False):
        self.opacity = 0
        self.speed = self.DEFAULT_FADE_SPEED
        self.timer.start()
        
    def fadeOut(self, force = False):
        self.opacity = self.FULL_THERSHOLD
        self.speed = -self.DEFAULT_FADE_SPEED
        self.timer.start()
        
    __color = QtGui.QColor(0, 0, 0)
    @property
    def color(self):
        return self.__color
    
    @color.setter       
    def color(self, value):
        assert isinstance(value, QtGui.QColor)
        self.__color = value
       
    __backgroundColor = QtGui.QColor(248, 240, 200)
    @property
    def backgroundColor(self):
        return self.__backgroundColor
    
    @backgroundColor.setter       
    def backgroundColor(self, value):
        assert isinstance(value, QtGui.QColor)
        self.__backgroundColor = value
        self._updateStylesheetAlpha()
    
    
    __borderColor = QtGui.QColor(173, 114, 47)
    @property
    def borderColor(self):
        return self.__borderColor
    
    @borderColor.setter       
    def borderColor(self, value):
        assert isinstance(value, QtGui.QColor)
        self.__borderColor = value
        self._updateStylesheetAlpha()
            
    __opacity = 1.0
    @property
    def opacity(self):
        return self.__opacity
    
    @opacity.setter       
    def opacity(self, value):
        assert value <= 1, "%s is not in 0..1 value" % value
        if value < 0:
            value = 0
        self.__opacity = value
        self._updateStylesheetAlpha()
    
    def mousePressEvent(self, event):
        self.messageClicked.emit()
    
    def updateOpacity(self):
        
        if self.speed > 0:
            if self.isHidden():
                self.show()
            if self.opacity <= self.FULL_THERSHOLD:
                self.opacity += self.speed
            else:
                self.timer.stop()
                self.fadedIn.emit()
                
        elif self.speed < 0:
            if self.opacity > 0:
                self.opacity += self.speed
            else:
                self.timer.stop()
                self.fadedOut.emit()
                self.hide()
    
    COLOR_PATTERN = re.compile(r"(?<!-)color:\s*rgba?\([\d\,\s\%\w]*\);?", re.MULTILINE | re.UNICODE)
    BACKGROUND_COLOR_PATTERN = re.compile(r"background-color:\s*rgba?\([\d\,\s\%\w]*\);?", re.MULTILINE | re.UNICODE)
    BORDER_COLOR_PATTERN = re.compile(r"border-color:\s*rgba?\([\d\,\s\%\w]*\);?", re.MULTILINE | re.UNICODE)
    
    def _updateStylesheetAlpha(self):
        styleSheet = unicode(self.styleSheet())
        #re.sub(pattern, repl, string, count, flags)
        
        for regex, name, col in ((self.COLOR_PATTERN, 'color', self.color),
                                 (self.BACKGROUND_COLOR_PATTERN, 'background-color',self.backgroundColor),
                                 (self.BORDER_COLOR_PATTERN, 'border-color', self.borderColor)):
            repl = '%s: rgba(%d, %d, %d, %d%%);' % (name, col.red(), col.green(), col.blue(), self.opacity * 100.0)
            styleSheet = regex.sub(repl, styleSheet)
        self.setStyleSheet(styleSheet)
    