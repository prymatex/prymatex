#!/usr/bin/env python

import collections

from prymatex.qt import QtCore, QtGui

class Notification(QtGui.QWidget):
    aboutToClose = QtCore.Signal()
    contentChanged = QtCore.Signal()
    def __init__(self, text, parent, timeout=None, icon=None, links=None):
        super(Notification, self).__init__(parent)

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.horizontalLayout = QtGui.QHBoxLayout(self)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setMargin(0)

        # ------------------- Elements
        self.pixmap = None
        if icon is not None:
            self.pixmap = QtGui.QLabel(self)
            self.pixmap.setPixmap(icon.pixmap(
                QtCore.QSize(
                    self.pixmap.height(),
                    self.pixmap.height()
                )
            ))
            self.pixmap.setAutoFillBackground(True)
            self.horizontalLayout.addWidget(self.pixmap)

        self.label = QtGui.QLabel(self)
        self.label.setText(text)
        self.label.setAutoFillBackground(True)
        self.horizontalLayout.addWidget(self.label)
        
        if links is not None:
            self.links = links
            self.label.linkActivated.connect(self.linkHandler)
        
        self.timeoutTimer = QtCore.QTimer(self)
        self.timeoutTimer.setSingleShot(True)
        
        # ---------- Animation
        #self.shadow = QtGui.QGraphicsDropShadowEffect()
        #self.shadow.setBlurRadius(10)
        self.goe = QtGui.QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.goe)
        
        # Fade in
        self.animationIn = QtCore.QPropertyAnimation(self.goe, "opacity")
        self.animationIn.setDuration(300)
        self.animationIn.setStartValue(0)
        self.animationIn.setEndValue(1.0)

        # Fade out
        self.animationOut = QtCore.QPropertyAnimation(self.goe, "opacity")
        self.animationOut.setDuration(300)
        self.animationOut.setStartValue(1.0)
        self.animationOut.setEndValue(0)

        if timeout is not None:
            self.timeoutTimer.setInterval(timeout)
            self.animationIn.finished.connect(self.timeoutTimer.start)
            self.timeoutTimer.timeout.connect(self.close)
            
    def setText(self, text):
        self.label.setText(text)
        self.adjustSize()
        self.contentChanged.emit()

    def applyStyle(self, background, foreground, padding = 5, border = 1,
            radius = 5):

        label_style =  "; ".join((
            "background-color: %s" % background,
            "color: %s" % foreground,
            "border-color: %s" % foreground,
            "border: %dpx solid %s" % (border, foreground),
            "padding: %dpx" % padding))
        if self.pixmap is not None:
            self.pixmap.setStyleSheet("; ".join((
                "background-color: %s" % background,
                "color: %s" % foreground,
                "border: %dpx solid %s" % (border, foreground),
                "border-right: 0px", 
                "padding: %dpx" % padding,
                "border-top-left-radius: %dpx" % radius,
                "border-bottom-left-radius: %dpx" % radius
            )))
            label_style = "; ".join((
                label_style,
                "border-left: 0px", 
                "border-top-right-radius: %dpx" % radius,
                "border-bottom-right-radius: %dpx" % radius
            ))
        else:
            label_style = "; ".join((
                label_style,
                "border-radius: %dpx" % radius))
        self.label.setStyleSheet(label_style)
    
    def show(self):
        self.setWindowOpacity(0.0)
        super(Notification, self).show()
        self.animationIn.start()
    
    def hide(self):
        self.animationOut.finished.connect(super(Notification, self).hide)
        self.animationOut.start()
    
    def close(self):
        self.aboutToClose.emit()
        self.animationOut.finished.connect(super(Notification, self).close)
        self.animationOut.start()
    
    def linkHandler(self, link):
        callback = self.links.get(link, None)
        if isinstance(callback, collections.Callable):
            callback()
    
    def enterEvent(self, event):
        if self.timeoutTimer.isActive():
            self.timeoutTimer.stop()
    
    def leaveEvent(self, event):
        self.timeoutTimer.start()

class OverlayNotifier(QtCore.QObject):
    margin = 10
    timeout = 2000
    def __init__(self, parent = None):
        super(OverlayNotifier, self).__init__(parent)
        parent.installEventFilter(self)
        self.notifications = []
        self.palette = QtGui.QPalette()
        self.font = QtGui.QFont()
        self.background_role = QtGui.QPalette.ToolTipBase
        self.foreground_role = QtGui.QPalette.ToolTipText

    def setFont(self, font):
        self.font = font

    def setBackgroundRole(self, role):
        self.background_role = role
        
    def setForegroundRole(self, role):
        self.foreground_role = role
        
    def setPalette(self, palette):
        self.palette = palette

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.Resize:
            self._fix_positions()
        return super(OverlayNotifier, self).eventFilter(obj, event)

    def _remove_notification(self):
        notification = self.sender()
        notification.aboutToClose.disconnect(self._remove_notification)
        notification.contentChanged.disconnect(self._fix_positions)
        self.notifications.remove(notification)
        self._fix_positions()
        
    def _fix_positions(self):
        offsets = {}
        for notification in self.notifications:
            parent = notification.parent()
            offset = offsets.setdefault(parent, self.margin)
            rect = parent.geometry()
            x = rect.width() - notification.width() - self.margin
            y = rect.height() - notification.height() - offset
            notification.setGeometry(x, y,
                notification.width(),
                notification.height())
            offsets[parent] += (notification.height() + self.margin)

    def _notification(self, message, title="", frmt="text", timeout=None, icon=None,
        links={}, widget = None):
        if title:
            title = "%s:\n" % title if frmt == "text" else "<h4>%s</h4>" % title
        message = title + message
        if frmt == "text" and links:
            message = "<pre>%s</pre>" % message
        if links:
            message += "<div style='text-align: right; font-size: small;'>"
            for key in links.keys():
                message += "<a href='%s'>%s</a>" % (key, key.title())
            message += "</div>"
        
        notification = Notification(message, 
            widget or self.parent(), 
            timeout, 
            icon, 
            links)

        # --------------- Style
        notification.setFont(self.font)
        background = self.palette.color(self.background_role).name()
        color = self.palette.color(self.foreground_role).name()
        notification.applyStyle(background, color)
        notification.adjustSize()
        return notification
        
    def message(self, *args, **kwargs):
        kwargs.setdefault("timeout", self.timeout)
        notification = self._notification(*args, **kwargs)
        notification.aboutToClose.connect(self._remove_notification)
        notification.contentChanged.connect(self._fix_positions)
        self.notifications.insert(0, notification)
        self._fix_positions()
        return notification

    def status(self, *args, **kwargs):
        notification = self._notification(*args, **kwargs)
        notification.aboutToClose.connect(self._remove_notification)
        notification.contentChanged.connect(self._fix_positions)
        self.notifications.insert(0, notification)
        self._fix_positions()
        return notification

    def tooltip(self, *args, **kwargs):
        kwargs.setdefault("timeout", self.timeout)
        point = kwargs.pop("point", QtCore.QPoint(self.margin,self.margin))
        notification = self._notification(*args, **kwargs)
        notification.setGeometry(point.x(), point.y(),
            notification.width(), notification.height())
        return notification
