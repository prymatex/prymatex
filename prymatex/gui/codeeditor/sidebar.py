#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from prymatex.qt import QtGui, QtCore

from prymatex import resources

from prymatex.core.settings import pmxConfigPorperty
from prymatex.core import PrymatexEditorAddon

class CodeEditorSideBar(QtGui.QWidget):
    updateRequest = QtCore.Signal()
    
    def __init__(self, editor):
        QtGui.QWidget.__init__(self, editor)
        self.editor = editor
        self.horizontalLayout = QtGui.QHBoxLayout(self)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setMargin(0)
        
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
        for index in range(self.horizontalLayout.count()):
            self.horizontalLayout.itemAt(index).widget().scroll(*largs)

#========================================
# BASE EDITOR SIDEBAR ADDON
#========================================
class SideBarWidgetAddon(PrymatexEditorAddon):
    ALIGNMENT = None

    def translatePosition(self, position):
        font_metrics = QtGui.QFontMetrics(self.editor.font())
        fh = font_metrics.lineSpacing()
        ys = position.y()
        
        block = self.editor.firstVisibleBlock()
        offset = self.editor.contentOffset()
        page_bottom = self.editor.viewport().height()
        while block.isValid():
            blockPosition = self.editor.blockBoundingGeometry(block).topLeft() + offset
            if blockPosition.y() > page_bottom:
                break
            if blockPosition.y() < ys and (blockPosition.y() + fh) > ys:
                break
            block = block.next()
        return block

#=======================================
# SideBar Widgets
#=======================================
class LineNumberSideBarAddon(SideBarWidgetAddon, QtGui.QWidget):
    ALIGNMENT = QtCore.Qt.AlignLeft
    MARGIN = 2

    @pmxConfigPorperty(default = True)
    def showLineNumbers(self, value):
        self.setVisible(value)
    
    def __init__(self, **kwargs):
        super(LineNumberSideBarAddon, self).__init__(**kwargs)
        self.setObjectName(self.__class__.__name__)

    def initialize(self, **kwargs):
        super(LineNumberSideBarAddon, self).initialize(**kwargs)
        
        self.__update_colours()
        self.__update_fonts()
        
        # Connect signals
        self.editor.themeChanged.connect(self.on_editor_themeChanged)
        self.editor.blockCountChanged.connect(self.on_editor_blockCountChanged)
        self.editor.fontChanged.connect(self.on_editor_fontChanged)
    
    def __update_colours(self):
        self.background = self.editor.colours['gutterBackground']
        self.foreground = self.editor.colours['gutterForeground']
        self.invisibles = self.editor.colours['invisibles']
        
    def __update_fonts(self):
        self.normalFont = QtGui.QFont(self.editor.font())
        self.boldFont = QtGui.QFont(self.editor.font())
        self.boldFont.setBold(True)
        self.normalMetrics = QtGui.QFontMetrics(self.normalFont)
        self.boldMetrics = QtGui.QFontMetrics(self.boldFont)
        self.__update_width()

    def __update_width(self, lineCount = None):
        lineCount = lineCount or self.editor.document().lineCount()
        width = self.boldMetrics.width(str(lineCount)) + self.MARGIN * 2
        if self.width() != width:
            self.setFixedWidth(width)
            self.editor.updateViewportMargins()
        
    def on_editor_themeChanged(self):
        self.__update_colours()

    def on_editor_blockCountChanged(self, newBlockCount):
        self.__update_width(newBlockCount)

    def on_editor_fontChanged(self):
        self.__update_fonts()
        
    @classmethod
    def contributeToMainMenu(cls):
        baseMenu = cls.ALIGNMENT == QtCore.Qt.AlignRight and "rightGutter" or "leftGutter"
        menuEntry = {
            'name': 'lineNumbers',
            'text': "Line numbers",
            'sequence': resources.get_sequence("SideBar", "ShowLineNumbers", 'F10'),
            'toggled': lambda instance, checked: instance.setVisible(checked),
            'testChecked': lambda instance: instance.isVisible() }
        return { baseMenu: menuEntry }

    def paintEvent(self, event):
        page_bottom = self.editor.viewport().height()
        current_block = self.editor.textCursor().block()
        
        painter = QtGui.QPainter(self)
        painter.setPen(self.foreground)
        painter.fillRect(self.rect(), self.background)
        painter.setFont(self.normalFont)
        
        block = self.editor.firstVisibleBlock()
        offset = self.editor.contentOffset()
        line_count = block.blockNumber()
        
        while block.isValid():
            line_count += 1
            # The top left position of the block in the document
            blockGeometry = self.editor.blockBoundingGeometry(block)
            blockGeometry.translate(offset)
            # Check if the position of the block is out side of the visible area
            if blockGeometry.top() > page_bottom:
                break

            # Draw the line number right justified at the y position of the line.
            if block.isVisible():
                numberText = str(line_count)
                if block == current_block:
                    painter.fillRect(blockGeometry, self.invisibles)
                    painter.setFont(self.boldFont)
                    leftPosition = self.width() - (self.boldMetrics.width(numberText) + self.MARGIN)
                    topPosition = blockGeometry.y() + self.boldMetrics.ascent()
                    painter.drawText(leftPosition, topPosition, numberText)
                    painter.setFont(self.normalFont)
                else:
                    leftPosition = self.width() - (self.normalMetrics.width(numberText) + self.MARGIN)
                    topPosition = blockGeometry.y() + self.normalMetrics.ascent()
                    painter.drawText(leftPosition, topPosition, numberText)
            
            block = block.next()

        painter.end()
        QtGui.QWidget.paintEvent(self, event)

class BookmarkSideBarAddon(SideBarWidgetAddon, QtGui.QWidget):
    ALIGNMENT = QtCore.Qt.AlignLeft
    
    @pmxConfigPorperty(default = False)
    def showBookmarks(self, value):
        self.setVisible(value)
    
    def __init__(self, **kwargs):
        super(BookmarkSideBarAddon, self).__init__(**kwargs)
        self.bookmarkflagImage = resources.get_image("bookmarkflag")
        self.imagesHeight = self.bookmarkflagImage.height()
        self.setFixedWidth(self.bookmarkflagImage.width())
        self.setObjectName(self.__class__.__name__)
        
    def initialize(self, **kwargs):
        super(BookmarkSideBarAddon, self).initialize(**kwargs)
        self.background = self.editor.colours['gutterBackground']
        self.foreground = self.editor.colours['gutterForeground']
        self.invisibles = self.editor.colours['invisibles']
        self.editor.themeChanged.connect(self.updateColours)
        
    def updateColours(self):
        self.background = self.editor.colours['gutterBackground']
        self.foreground = self.editor.colours['gutterForeground']
        self.invisibles = self.editor.colours['invisibles']
        self.repaint(self.rect())

    @classmethod
    def contributeToMainMenu(cls):
        baseMenu = cls.ALIGNMENT == QtCore.Qt.AlignRight and "rightGutter" or "leftGutter"
        menuEntry = {
            'name': 'bookmarks',
            'text': "Bookmarks",
            'sequence': resources.get_sequence("SideBar", "ShowBookmarks", 'Alt+F10'),
            'toggled': lambda instance, checked: instance.setVisible(checked),
            'testChecked': lambda instance: instance.isVisible() }
        return { baseMenu: menuEntry} 
            
    def paintEvent(self, event):
        font_metrics = QtGui.QFontMetrics(self.editor.font())
        page_bottom = self.editor.viewport().height()
        current_block = self.editor.textCursor().block()
        
        painter = QtGui.QPainter(self)
        painter.fillRect(self.rect(), self.background)

        block = self.editor.firstVisibleBlock()
        offset = self.editor.contentOffset()
        
        while block.isValid():
            blockGeometry = self.editor.blockBoundingGeometry(block)
            blockGeometry.translate(offset)
            # Check if the position of the block is out side of the visible area
            if blockGeometry.top() > page_bottom:
                break
            
            if block == current_block:
                painter.fillRect(blockGeometry, self.invisibles)

            # Draw the line number right justified at the y position of the line.
            if block.isVisible() and block in self.editor.bookmarkListModel:
                positionY = blockGeometry.top() + ((blockGeometry.height() - self.imagesHeight) / 2)
                painter.drawPixmap(0, positionY, self.bookmarkflagImage)

            block = block.next()

        painter.end()
        QtGui.QWidget.paintEvent(self, event)
        
    def mousePressEvent(self, event):
        block = self.translatePosition(event.pos())
        cursor = self.editor.newCursorAtPosition(block.position())
        self.editor.toggleBookmark(cursor)
        self.repaint(self.rect())
            
class FoldingSideBarAddon(SideBarWidgetAddon, QtGui.QWidget):
    ALIGNMENT = QtCore.Qt.AlignLeft
    
    @pmxConfigPorperty(default = True)
    def showFolding(self, value):
        self.setVisible(value)

    def __init__(self, **kwargs):
        super(FoldingSideBarAddon, self).__init__(**kwargs)
        self.foldingcollapsedImage = resources.get_image("foldingcollapsed")
        self.foldingtopImage = resources.get_image("foldingtop")
        self.foldingbottomImage = resources.get_image("foldingbottom")
        self.imagesHeight = self.foldingcollapsedImage.height()
        self.setFixedWidth(self.foldingbottomImage.width())
        self.setObjectName(self.__class__.__name__)

    def initialize(self, **kwargs):
        super(FoldingSideBarAddon, self).initialize(**kwargs)
        self.background = self.editor.colours['gutterBackground']
        self.invisibles = self.editor.colours['invisibles']
        self.editor.themeChanged.connect(self.updateColours)
        
    def updateColours(self):
        self.background = self.editor.colours['gutterBackground']
        self.invisibles = self.editor.colours['invisibles']
        self.repaint(self.rect())
    
    @classmethod
    def contributeToMainMenu(cls):
        baseMenu = cls.ALIGNMENT == QtCore.Qt.AlignRight and "rightGutter" or "leftGutter"
        menuEntry = {
            'name': 'foldings',
            'text': 'Foldings',
            'sequence': resources.get_sequence("SideBar", "ShowFoldings", 'Shift+F10'),
            'toggled': lambda instance, checked: instance.setVisible(checked),
            'testChecked': lambda instance: instance.isVisible() }
        return {baseMenu: menuEntry} 
    
    def paintEvent(self, event):
        font_metrics = QtGui.QFontMetrics(self.editor.font())
        page_bottom = self.editor.viewport().height()
        current_block = self.editor.textCursor().block()
        
        painter = QtGui.QPainter(self)
        painter.fillRect(self.rect(), self.background)

        block = self.editor.firstVisibleBlock()
        offset = self.editor.contentOffset()
        
        while block.isValid():
            blockGeometry = self.editor.blockBoundingGeometry(block)
            blockGeometry.translate(offset)
            
            # Check if the position of the block is out side of the visible area
            if blockGeometry.top() > page_bottom:
                break

            if block == current_block:
                painter.fillRect(blockGeometry, self.invisibles)

            # Draw the line number right justified at the y position of the line.
            if block.isVisible():
                positionY = blockGeometry.top() + ((blockGeometry.height() - self.imagesHeight) / 2)
                if self.editor.isFoldingStartMarker(block) or self.editor.isFoldingIndentedBlockStart(block):
                    if self.editor.isFolded(block):
                        painter.drawPixmap(0, positionY, self.foldingcollapsedImage)
                    else:
                        painter.drawPixmap(0, positionY, self.foldingtopImage)
                elif self.editor.isFoldingStopMarker(block):
                    painter.drawPixmap(0, positionY, self.foldingbottomImage)

            block = block.next()

        painter.end()
        QtGui.QWidget.paintEvent(self, event)
        
    def mousePressEvent(self, event):
        block = self.translatePosition(event.pos())
        if self.editor.isFolded(block):
            self.editor.codeFoldingUnfold(block)
        else:
            self.editor.codeFoldingFold(block)

class SelectionSideBarAddon(SideBarWidgetAddon, QtGui.QWidget):
    ALIGNMENT = QtCore.Qt.AlignRight
    
    @pmxConfigPorperty(default = False)
    def showSelection(self, value):
        self.setVisible(value)
    
    def __init__(self, **kwargs):
        super(SelectionSideBarAddon, self).__init__(**kwargs)
        self.setFixedWidth(10)
        self.setObjectName(self.__class__.__name__)
        
    def initialize(self, **kwargs):
        super(SelectionSideBarAddon, self).initialize(**kwargs)
        self.background = self.editor.colours['gutterBackground']
        self.editor.themeChanged.connect(self.updateColours)
        self.editor.extraSelectionChanged.connect(self.on_editor_extraSelectionChanged)
        
    def updateColours(self):
        self.background = self.editor.colours['gutterBackground']
        self.update()
    
    def on_editor_extraSelectionChanged(self):
        self.update()

    @classmethod
    def contributeToMainMenu(cls):
        baseMenu = cls.ALIGNMENT == QtCore.Qt.AlignRight and "rightGutter" or "leftGutter"
        menuEntry = {
            'name': 'selection',
            'text': 'Selection',
            'toggled': lambda instance, checked: instance.setVisible(checked),
            'testChecked': lambda instance: instance.isVisible() }
        return { baseMenu: menuEntry }
    
    def paintEvent(self, event):
        font_metrics = QtGui.QFontMetrics(self.editor.font())
        page_bottom = self.editor.viewport().height()
        
        lineHeight = font_metrics.height()

        scrollBar = self.editor.verticalScrollBar()
        if scrollBar.isVisible():
            rectRelation = float(scrollBar.height()) / float(self.editor.document().blockCount())
        else:
            rectRelation = lineHeight
        rectHeight = round(rectRelation) if rectRelation >= 1 else 1

        painter = QtGui.QPainter(self)
        painter.fillRect(self.rect(), self.background)

        offset = self.editor.contentOffset()

        for extra in self.editor.searchExtraSelections("selection"):
            y = round(extra.cursor.block().blockNumber() * rectRelation)
            if rectRelation == lineHeight:
                y += offset.y()
            painter.fillRect(0, y, 10, rectHeight, self.editor.colours['selection'])

        painter.end()
        QtGui.QWidget.paintEvent(self, event)
        
    def mousePressEvent(self, event):
        block = self.translatePosition(event.pos())
        print(block)
