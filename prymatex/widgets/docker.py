#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from prymatex.qt import QtCore, QtGui, QtWidgets

def hasFeature(dockwidget, feature):
    return dockwidget.features() & feature == feature

class DockWidgetTitleBarButton(QtWidgets.QAbstractButton):
    def __init__(self, titlebar):
        super(DockWidgetTitleBarButton, self).__init__(titlebar)
        self.setFocusPolicy(QtCore.Qt.NoFocus)

    def sizeHint(self):
        self.ensurePolished()
        margin = self.style().pixelMetric(QtWidgets.QStyle.PM_DockWidgetTitleBarButtonMargin, None, self)
        if self.icon().isNull():
            return QtCore.QSize(margin, margin)
        iconSize = self.style().pixelMetric(QtWidgets.QStyle.PM_SmallIconSize, None, self)
        pm = self.icon().pixmap(iconSize)
        return QtCore.QSize(pm.width() + margin, pm.height() + margin)

    def enterEvent(self, event):
        if self.isEnabled():
            self.update()
        QtWidgets.QAbstractButton.enterEvent(self, event)

    def leaveEvent(self, event):
        if self.isEnabled():
            self.update()
        QtWidgets.QAbstractButton.leaveEvent(self, event)

    def paintEvent(self, event):
        p = QtGui.QPainter(self)
        r = self.rect()
        opt = QtWidgets.QStyleOptionToolButton()
        opt.init(self)
        opt.state |= QtWidgets.QStyle.State_AutoRaise
        if self.isEnabled() and self.underMouse() and \
           not self.isChecked() and not self.isDown():
            opt.state |= QtWidgets.QStyle.State_Raised
        if self.isChecked():
            opt.state |= QtWidgets.QStyle.State_On
        if self.isDown():
            opt.state |= QtWidgets.QStyle.State_Sunken
        self.style().drawPrimitive(
            QtWidgets.QStyle.PE_PanelButtonTool, opt, p, self)
        opt.icon = self.icon()
        opt.subControls = QtWidgets.QStyle.SubControls()
        opt.activeSubControls = QtWidgets.QStyle.SubControls()
        #opt.features = QtWidgets.QStyleOptionToolButton.None
        opt.arrowType = QtCore.Qt.NoArrow
        size = self.style().pixelMetric(QtWidgets.QStyle.PM_SmallIconSize, None, self)
        opt.iconSize = QtCore.QSize(size, size)
        self.style().drawComplexControl(QtWidgets.QStyle.CC_ToolButton, opt, p, self)

class DockWidgetTitleBar(QtWidgets.QWidget):
    collpaseAreaRequest = QtCore.Signal(QtWidgets.QDockWidget)
    
    def __init__(self, dockWidget):
        QtWidgets.QWidget.__init__(self, dockWidget)
        self.floatButton = DockWidgetTitleBarButton(self)
        self.floatButton.setIcon(dockWidget.resources().get_icon("TitleBarNormalButton"))
        self.floatButton.clicked.connect(self.toggleFloating)
        self.floatButton.setVisible(True)
        self.closeButton = DockWidgetTitleBarButton(self)
        self.closeButton.setIcon(dockWidget.resources().get_icon("TitleBarCloseButton"))
        self.closeButton.clicked.connect(dockWidget.close)
        self.closeButton.setVisible(True)
        self.collapseButton = DockWidgetTitleBarButton(self)
        self.collapseButton.setIcon(dockWidget.resources().get_icon("TitleBarMinButton"))
        self.collapseButton.clicked.connect(self._collapse_area_request)
        self.collapseButton.setVisible(True)
        dockWidget.featuresChanged.connect(self.featuresChanged)
        self.featuresChanged(0)

    def _collapse_area_request(self):
        self.collpaseAreaRequest.emit(self.parentWidget())
        
    def minimumSizeHint(self):
        return self.sizeHint()

    def sizeHint(self):
        q = self.parentWidget()
        mw = q.style().pixelMetric(QtWidgets.QStyle.PM_DockWidgetTitleMargin, None, q)
        fw = q.style().pixelMetric(QtWidgets.QStyle.PM_DockWidgetFrameWidth, None, q)
        closeSize = QtCore.QSize(0, 0)
        if self.closeButton:
            closeSize = self.closeButton.sizeHint()
        floatSize = QtCore.QSize(0, 0)
        if self.floatButton:
            floatSize = self.floatButton.sizeHint()
        hideSize = QtCore.QSize(0, 0)
        if self.collapseButton:
            hideSize = self.collapseButton.sizeHint()
        buttonHeight = max(max(closeSize.height(), floatSize.height()), hideSize.height()) + 2
        buttonWidth = closeSize.width() + floatSize.width() + hideSize.width()
        titleFontMetrics = q.fontMetrics()
        fontHeight = titleFontMetrics.lineSpacing() + 2 * mw
        height = max(buttonHeight, fontHeight)
        return QtCore.QSize(buttonWidth + height + 4 * mw + 2 * fw, height)

    def paintEvent(self, event):
        p = QtWidgets.QStylePainter(self)
        q = self.parentWidget()
        fw = q.isFloating() and q.style().pixelMetric(QtWidgets.QStyle.PM_DockWidgetFrameWidth, None, q) or 0
        mw = q.style().pixelMetric(QtWidgets.QStyle.PM_DockWidgetTitleMargin, None, q)
        titleOpt = QtWidgets.QStyleOptionDockWidgetV2()
        titleOpt.initFrom(q)
        titleOpt.rect = QtCore.QRect(QtCore.QPoint(fw + mw + self.collapseButton.size().width(), fw),
            QtCore.QSize(
               self.geometry().width() - (fw * 2) - \
               mw - self.collapseButton.size().width(),
               self.geometry().height() - (fw * 2)))
        titleOpt.title = q.windowTitle()
        titleOpt.closable = hasFeature(q, QtWidgets.QDockWidget.DockWidgetClosable)
        titleOpt.floatable = hasFeature(q, QtWidgets.QDockWidget.DockWidgetFloatable)
        p.drawControl(QtWidgets.QStyle.CE_DockWidgetTitle, titleOpt)

    def resizeEvent(self, event):
        q = self.parentWidget()
        fw = q.isFloating() and q.style().pixelMetric(
            QtWidgets.QStyle.PM_DockWidgetFrameWidth, None, q) or 0
        opt = QtWidgets.QStyleOptionDockWidgetV2()
        opt.initFrom(q)
        opt.rect = QtCore.QRect(
            QtCore.QPoint(fw, fw),
            QtCore.QSize(
              self.geometry().width() - (fw * 2),
              self.geometry().height() - (fw * 2)))
        opt.title = q.windowTitle()
        opt.closable = hasFeature(q, QtWidgets.QDockWidget.DockWidgetClosable)
        opt.floatable = hasFeature(q, QtWidgets.QDockWidget.DockWidgetFloatable)

        floatRect = q.style().subElementRect(
            QtWidgets.QStyle.SE_DockWidgetFloatButton, opt, q)
        if not floatRect.isNull():
            self.floatButton.setGeometry(floatRect)
        closeRect = q.style().subElementRect(
        QtWidgets.QStyle.SE_DockWidgetCloseButton, opt, q)
        if not closeRect.isNull():
            self.closeButton.setGeometry(closeRect)
        top = fw
        if not floatRect.isNull():
            top = floatRect.y()
        elif not closeRect.isNull():
            top = closeRect.y()
        size = self.collapseButton.size()
        if not closeRect.isNull():
            size = self.closeButton.size()
        elif not floatRect.isNull():
            size = self.floatButton.size()
        collapseRect = QtCore.QRect(QtCore.QPoint(fw, top), size)
        self.collapseButton.setGeometry(collapseRect)

    def toggleFloating(self):
        q = self.parentWidget()
        q.setFloating(not q.isFloating())

    def toggleFloating(self):
        q = self.parentWidget()
        q.setFloating(not q.isFloating())

    def featuresChanged(self, features):
        q = self.parentWidget()
        self.closeButton.setVisible(hasFeature(q, QtWidgets.QDockWidget.DockWidgetClosable))
        self.floatButton.setVisible(hasFeature(q, QtWidgets.QDockWidget.DockWidgetFloatable))
