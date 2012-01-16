import re

from PyQt4 import QtCore, QtGui

from prymatex.core.plugin import PMXBaseOverlay
    
class PMXMessageOverlay(QtGui.QLabel, PMXBaseOverlay):
    ''' 
    Inner message QLabel.
    StyleSheet
    Don't use this widget separately, please use PMXMessageOverlay API
    '''
    fadedOut = QtCore.pyqtSignal()
    fadedIn = QtCore.pyqtSignal()
    messageClicked = QtCore.pyqtSignal()
    mouseIn = QtCore.pyqtSignal()
    
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
    
    __position = None
    @property
    def position(self):
        return self.__position
    
    @position.setter       
    def position(self, value):
        if isinstance(value, QtCore.QPoint):
            value = (value.x(), value.y())
        elif value is not None:
            assert len(value) == 2
            assert type(value[0]) in (int, float)
            assert type(value[1]) in (int, float)
        self.__position = value
    
    # Padding
    paddingLeft = 10
    # Padding
    paddingBottom = 10
    # When mouse gets in
    mousePreventsFadeout = True
    
    _hovered = False
    
    def __init__(self, parent):
        '''
        This label is managed from PMXMessageOverlay mixin, should not be
        used outside this module
        '''
        QtGui.QLabel.__init__(self, parent)
        
        self.fadeOutTimer = QtCore.QTimer(self)
        self.fadeOutTimer.timeout.connect(self.fadeOut)
        self.mouseIn.connect(self.fadeOutTimer.stop)
        
        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(32)
        self.timer.timeout.connect(self.updateOpacity)
        self.speed = 0
        self.setStyleSheet(self.STYLESHEET)
        self.opacity = 0
        self.linkActivated.connect(self.linkHandler)

    def showMessage(self, message, timeout = 2000, icon = None, pos = None, hrefCallbacks = {} ):
        '''
        @param message: Text message, can be HTML
        @param timeout: Timeout before message fades
        @param icon: A QIcon instance to show
        @param pos: An x, y tuple with message position
        @param link_map: 
        '''
        self.setText(message)
        self.position = pos
        self.updatePosition()
        self.adjustSize()
        self.linkMap = hrefCallbacks
        if unicode(message):
            self.fadeIn()
            if timeout:
                print "Launching fadeout timer"
                self.fadeOutTimer.start(timeout)
        else:
            self.fadeOutTimer.stop()
            self.fadeOut()

    def clearMessage(self):
        self.fadeOut()
    
    def messageClicked(self):
        ''' Overrride '''
        self.clearMessage()       
        
    def updateOverlay(self):
        ''' Override '''
        self.updatePosition()
    
    def linkHandler(self, link):
        callback = self.linkMap.get(link, None)
        if callback is None:
            self.logger.warn("No callback for %s" % link)
            return
        if not callable(callback):
            self.logger.warn("Callback for %s is not callable: %s" % (link, callback))
            return
        
        self.logger.debug( "Running callback: %s %s" % (link, callback))
        callback()
  
    def setText(self, text):
        QtGui.QLabel.setText(self, text)
        self._hovered = False
        self.linkMap = {}

    def updatePosition(self):
        if self.position is not None:
            x, y = self.position
        else:
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
        QtGui.QLabel.resizeEvent(self, event)
        self.updatePosition()
    
    def showEvent(self, event):
        self.updatePosition()
        return QtGui.QLabel.showEvent(self, event)
  
    def enterEvent(self, event):
        """ Mouse hovered the messge """
        if self.mousePreventsFadeout:
            self._hovered = True
            self.mouseIn.emit()
    
    def leaveEvent(self, event):
        ''' Leave '''
        if self.isVisible() and self._hovered:
            self.fadeOut()
    
    def mousePressEvent(self, event):
        self.messageClicked.emit()
    
    __linkMap = {}
    @property
    def linkMap(self):
        return self.__linkMap
    
    @linkMap.setter       
    def linkMap(self, value):
        for href, callback in value.iteritems():
            assert isinstance(href, basestring), "%s is not valid map"
            assert callable(callback), "%s is not valid callback (under %s)" % (callback, value)
        self.__linkMap = value
    
    #===========================================================================
    # Transparency handling
    #===========================================================================
    
    # Maximum transparency level
    FULL_THERSHOLD = 0.7
    # Transparency increment (linear transition)
    DEFAULT_FADE_SPEED = 0.15
    
    def fadeIn(self, force = False):
        ''' Triggers transparency fade in transition '''
        self.opacity = 0
        self.speed = self.DEFAULT_FADE_SPEED
        self.timer.start()
        
    def fadeOut(self, force = False):
        ''' Triggers transparency fade out transition '''
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
    
    #===========================================================================
    # Label Colors
    #===========================================================================
    def setMessageTextColor(self, color):
        self.color = color
    
    def setMessageBackgroundColor(self, color):
        self.backgroundColor = color
        
    def setMessageBorderColor(self, color):
        self.borderColor = color
    