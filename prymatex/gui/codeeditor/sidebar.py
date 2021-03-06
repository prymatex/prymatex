#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from prymatex.qt import QtCore, QtGui, QtWidgets

from prymatex.core.settings import ConfigurableItem
from prymatex.core import PrymatexEditorAddon

class CodeEditorSideBar(QtWidgets.QWidget):
    updateRequest = QtCore.Signal()
    
    def __init__(self, editor):
        super(CodeEditorSideBar, self).__init__(editor)
        self.editor = editor
        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setContentsMargins(0,0,0,0)

    def addWidget(self, widget):
        self.horizontalLayout.addWidget(widget)
        widget.installEventFilter(self)

    def eventFilter(self, obj, event):
        if event.type() in [ QtCore.QEvent.Hide, QtCore.QEvent.Show ]:
            self.updateRequest.emit()
            return True
        return QtCore.QObject.eventFilter(self, obj, event)

    def width(self):
        width = 0
        for index in range(self.horizontalLayout.count()):
            widget = self.horizontalLayout.itemAt(index).widget()
            if widget.isVisible():
                width += widget.width()
        return width

    def scroll(self, *largs):
        # TODO Solo si el widget es scrolleable
        for index in range(self.horizontalLayout.count()):
            self.horizontalLayout.itemAt(index).widget().scroll(*largs)

# ----------------- BASE EDITOR SIDEBAR ADDON
class SideBarWidgetMixin(PrymatexEditorAddon):
    ALIGNMENT = None

    def setPalette(self, palette):
        super(SideBarWidgetMixin, self).setPalette(palette)
        
    def setFont(self, font):
        super(SideBarWidgetMixin, self).setFont(font)
        self.normalFont = QtGui.QFont(font)
        self.boldFont = QtGui.QFont(font)
        self.boldFont.setBold(True)

# ------------------- SideBar Widgets
class LineNumberSideBarAddon(SideBarWidgetMixin, QtWidgets.QWidget):
    ALIGNMENT = QtCore.Qt.AlignLeft
    MARGIN = 2

    @ConfigurableItem(default = True)
    def showLineNumbers(self, value):
        self.setVisible(value)
    
    def __init__(self, **kwargs):
        super(LineNumberSideBarAddon, self).__init__(**kwargs)
        self.setObjectName(self.__class__.__name__)

    def initialize(self, **kwargs):
        super(LineNumberSideBarAddon, self).initialize(**kwargs)
        
        # Connect signals
        self.editor.blockCountChanged.connect(self.__update_width)

    def setFont(self, font):
        super(LineNumberSideBarAddon, self).setFont(font)
        self.__update_width(self.editor.document().lineCount())
        
    def __update_width(self, lineCount):
        width = self.fontMetrics().width("%s" % lineCount) + self.MARGIN * 2
        if self.width() != width:
            self.setFixedWidth(width)
            self.editor.updateViewportMargins()
    
    @classmethod
    def contributeToMainMenu(cls):
        baseMenu = cls.ALIGNMENT == QtCore.Qt.AlignRight and "Right Gutter" or "Left Gutter"
        menuEntry = {
            'text': "Line numbers",
            'checkable': True,
            'sequence': ("SideBar", "ShowLineNumbers", 'F10'),
            'triggered': lambda instance, checked: instance.setVisible(checked),
            'testChecked': lambda instance: instance.isVisible() }
        return { baseMenu: menuEntry }

    def paintEvent(self, event):
        page_bottom = self.editor.viewport().height()
        current_block = self.editor.textCursor().block()
        
        painter = QtGui.QPainter(self)
        painter.setPen(self.palette().toolTipText().color())
        painter.fillRect(self.rect(), self.palette().toolTipBase().color())
        
        block = self.editor.firstVisibleBlock()
        offset = self.editor.contentOffset()
        line_count = block.blockNumber()

        while block.isValid():
            line_count += 1

            # The top left position of the block in the document
            block_geometry = self.editor.blockBoundingGeometry(block)
            block_geometry.translate(offset)
            if block_geometry.top() > page_bottom:
                break

            if block.isVisible():
                text = "%d" % line_count
                painter.setFont(
                    block == current_block and self.boldFont or self.normalFont)
                metrics = painter.fontMetrics()
                color = (block == current_block and \
                    self.palette().alternateBase() or \
                    self.palette().toolTipBase()).color()
                painter.fillRect(
                    block_geometry.x(),
                    block_geometry.y(),
                    self.width(),
                    metrics.height(),
                    color)
                left_position = self.width() - (metrics.width(text) + self.MARGIN)
                top_position = block_geometry.y() + metrics.ascent()
                painter.drawText(left_position, top_position, text)
            
            # Setup painter and geometry again
            block = block.next()

        painter.end()
        QtWidgets.QWidget.paintEvent(self, event)

class BookmarkSideBarAddon(SideBarWidgetMixin, QtWidgets.QWidget):
    ALIGNMENT = QtCore.Qt.AlignLeft
    
    @ConfigurableItem(default = False)
    def showBookmarks(self, value):
        self.setVisible(value)
    
    def __init__(self, **kwargs):
        super(BookmarkSideBarAddon, self).__init__(**kwargs)
        self.bookmarkflagImage = self.resources().get_image("bookmark")
        self.imagesHeight = self.bookmarkflagImage.height()
        self.setFixedWidth(self.bookmarkflagImage.width())
        self.setObjectName(self.__class__.__name__)

    @classmethod
    def contributeToMainMenu(cls):
        baseMenu = cls.ALIGNMENT == QtCore.Qt.AlignRight and "Right Gutter" or "Left Gutter"
        menuEntry = {
            'text': "Bookmarks",
            'sequence': ("SideBar", "ShowBookmarks", 'Alt+F10'),
            'checkable': True,
            'triggered': lambda instance, checked: instance.setVisible(checked),
            'testChecked': lambda instance: instance.isVisible() }
        return { baseMenu: menuEntry} 
            
    def paintEvent(self, event):
        page_bottom = self.editor.viewport().height()
        current_block = self.editor.textCursor().block()

        painter = QtGui.QPainter(self)
        painter.fillRect(self.rect(), self.palette().toolTipBase().color())

        block = self.editor.firstVisibleBlock()
        offset = self.editor.contentOffset()
        
        while block.isValid():
            blockGeometry = self.editor.blockBoundingGeometry(block)
            blockGeometry.translate(offset)
            # Check if the position of the block is out side of the visible area
            if blockGeometry.top() > page_bottom:
                break
            
            if block.isVisible():
                painter.setFont(
                    block == current_block and self.boldFont or self.normalFont)
                metrics = painter.fontMetrics()
                color = (block == current_block and \
                    self.palette().alternateBase() or \
                    self.palette().toolTipBase()).color()
                painter.fillRect(
                    block_geometry.x(),
                    block_geometry.y(),
                    self.width(),
                    metrics.height(),
                    color)
    
                # Draw the line number right justified at the y position of the line.
                if self.editor.bookmarkListModel.bookmarksCount(block) > 0:
                    positionY = blockGeometry.top() + ((metrics.height() - self.imagesHeight) / 2)
                    painter.drawPixmap(0, positionY, self.bookmarkflagImage)

            block = block.next()

        painter.end()
        QtWidgets.QWidget.paintEvent(self, event)
        
    def mousePressEvent(self, event):
        cursor = self.editor.cursorForPosition(event.pos())
        self.editor.toggleBookmark(cursor)
        self.repaint(self.rect())
            
class FoldingSideBarAddon(SideBarWidgetMixin, QtWidgets.QWidget):
    ALIGNMENT = QtCore.Qt.AlignLeft
    
    @ConfigurableItem(default = True)
    def showFolding(self, value):
        self.setVisible(value)

    def __init__(self, **kwargs):
        super(FoldingSideBarAddon, self).__init__(**kwargs)
        self.foldingcollapsedImage = self.resources().get_image(":/sidebar/folding-collapsed.png")
        self.foldingtopImage = self.resources().get_image(":/sidebar/folding-top.png")
        self.foldingbottomImage = self.resources().get_image(":/sidebar/folding-bottom.png")
        self.imagesHeight = self.foldingcollapsedImage.height()
        self.setFixedWidth(self.foldingbottomImage.width())
        self.setObjectName(self.__class__.__name__)

    @classmethod
    def contributeToMainMenu(cls):
        baseMenu = cls.ALIGNMENT == QtCore.Qt.AlignRight and "Right Gutter" or "Left Gutter"
        menuEntry = {
            'text': 'Foldings',
            'sequence': ("SideBar", "ShowFoldings", 'Shift+F10'),
            'checkable': True,
            'triggered': lambda instance, checked: instance.setVisible(checked),
            'testChecked': lambda instance: instance.isVisible() }
        return {baseMenu: menuEntry} 
    
    def paintEvent(self, event):
        page_bottom = self.editor.viewport().height()
        current_block = self.editor.textCursor().block()
        
        painter = QtGui.QPainter(self)
        painter.fillRect(self.rect(), self.palette().toolTipBase().color())

        block = self.editor.firstVisibleBlock()
        offset = self.editor.contentOffset()
        
        while block.isValid():
            block_geometry = self.editor.blockBoundingGeometry(block)
            block_geometry.translate(offset)
            
            # Check if the position of the block is out side of the visible area
            if block_geometry.top() > page_bottom:
                break
            
            if block.isVisible():
                painter.setFont(
                    block == current_block and self.boldFont or self.normalFont)
                metrics = painter.fontMetrics()
                color = (block == current_block and \
                    self.palette().alternateBase() or \
                    self.palette().toolTipBase()).color()
                painter.fillRect(
                    block_geometry.x(),
                    block_geometry.y(),
                    self.width(),
                    metrics.height(),
                    color)
                
                cursor = self.editor.newCursorAtPosition(block.position())
                image = None
                if self.editor.foldingListModel.isStart(cursor):
                    if self.editor.foldingListModel.isFolded(cursor):
                        image = self.foldingcollapsedImage
                    else:
                        image = self.foldingtopImage
                elif self.editor.foldingListModel.isStop(cursor):
                    image = self.foldingbottomImage
                if image is not None:
                    positionY = block_geometry.top() + ((metrics.height() - self.imagesHeight) / 2)
                    painter.drawPixmap(0, positionY, image)

            block = block.next()

        painter.end()
        QtWidgets.QWidget.paintEvent(self, event)
        
    def mousePressEvent(self, event):
        cursor = self.editor.cursorForPosition(event.pos())
        self.editor.toggleFolding(cursor)

class SelectionSideBarAddon(SideBarWidgetMixin, QtWidgets.QWidget):
    ALIGNMENT = QtCore.Qt.AlignRight
    
    @ConfigurableItem(default = False)
    def showSelection(self, value):
        self.setVisible(value)
    
    def __init__(self, **kwargs):
        super(SelectionSideBarAddon, self).__init__(**kwargs)
        self.setFixedWidth(10)
        self.setObjectName(self.__class__.__name__)
        
    def initialize(self, **kwargs):
        super(SelectionSideBarAddon, self).initialize(**kwargs)
        self.editor.extraSelectionChanged.connect(self.on_editor_extraSelectionChanged)
        
    def on_editor_extraSelectionChanged(self):
        self.update()

    @classmethod
    def contributeToMainMenu(cls):
        baseMenu = cls.ALIGNMENT == QtCore.Qt.AlignRight and "Right Gutter" or "Left Gutter"
        menuEntry = {
            'text': 'Selection',
            'checkable': True,
            'triggered': lambda instance, checked: instance.setVisible(checked),
            'testChecked': lambda instance: instance.isVisible() }
        return { baseMenu: menuEntry }
    
    def paintEvent(self, event):
        page_bottom = self.editor.viewport().height()
        line_height = self.fontMetrics().height()

        scrollBar = self.editor.verticalScrollBar()
        if scrollBar.isVisible():
            rectRelation = float(scrollBar.height()) / float(self.editor.document().blockCount())
        else:
            rectRelation = line_height
        rectHeight = round(rectRelation) if rectRelation >= 1 else 1

        painter = QtGui.QPainter(self)
        painter.fillRect(self.rect(), self.palette().toolTipText().color())

        offset = self.editor.contentOffset()

        for cursor in self.editor.highlightCursors():
            y = round(cursor.block().blockNumber() * rectRelation)
            if rectRelation == line_height:
                y += offset.y()
            painter.fillRect(0, y, 10, rectHeight, self.palette().highlight().color())

        painter.end()
        QtWidgets.QWidget.paintEvent(self, event)
        
    def mousePressEvent(self, event):
        cursor = self.editor.cursorForPosition(event.pos())
        print(cursor)
 
