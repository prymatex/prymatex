#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from prymatex.qt import QtGui, QtCore

from prymatex import resources

from prymatex.core.settings import pmxConfigPorperty
from prymatex.core import PMXBaseEditorAddon

class CodeEditorSideBar(QtGui.QWidget):
    updateRequest = QtCore.pyqtSignal()
    
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
class SideBarWidgetAddon(PMXBaseEditorAddon):
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
class LineNumberSideBarAddon(QtGui.QWidget, SideBarWidgetAddon):
    ALIGNMENT = QtCore.Qt.AlignLeft
    MARGIN = 2

    @pmxConfigPorperty(default = True)
    def showLineNumbers(self, value):
        self.setVisible(value)
    
    def __init__(self, parent):
        QtGui.QWidget.__init__(self, parent)
        self.setObjectName(self.__class__.__name__)

    def initialize(self, editor):
        SideBarWidgetAddon.initialize(self, editor)
        
        self.__update_colours()
        self.__update_fonts()
        
        # Connect signals
        self.editor.themeChanged.connect(self.on_editor_themeChanged)
        self.editor.blockCountChanged.connect(self.on_editor_blockCountChanged)
        self.editor.fontChanged.connect(self.on_editor_fontChanged)
    
    def __update_colours(self):
        self.background = self.editor.colours['gutter']
        self.foreground = self.editor.colours['gutterForeground']
        
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
        def on_actionShowLineNumbers_toggled(editor, checked):
            instance = editor.findChild(cls, cls.__name__)
            if instance is not None:
                instance.setVisible(checked)

        def on_actionShowLineNumbers_testChecked(editor):
            instance = editor.findChild(cls, cls.__name__)
            return instance is not None and instance.isVisible()
        
        baseMenu = ("view", cls.ALIGNMENT == QtCore.Qt.AlignRight and "Right Gutter" or "Left Gutter")
        menuEntry = {
            'name': 'lineNumbers',
            'text': "Line Numbers",
            'callback': on_actionShowLineNumbers_toggled,
            'shortcut': 'F10',
            'checkable': True,
            'testChecked': on_actionShowLineNumbers_testChecked }
        return { baseMenu: menuEntry }

    def paintEvent(self, event):
        page_bottom = self.editor.viewport().height()
        current_block = self.editor.document().findBlock(self.editor.textCursor().position())
        
        painter = QtGui.QPainter(self)
        painter.setPen(self.foreground)
        painter.fillRect(self.rect(), self.background)

        block = self.editor.firstVisibleBlock()
        viewport_offset = self.editor.contentOffset()
        line_count = block.blockNumber()
        
        while block.isValid():
            line_count += 1
            # The top left position of the block in the document
            position = self.editor.blockBoundingGeometry(block).topLeft() + viewport_offset
            # Check if the position of the block is out side of the visible area
            if position.y() > page_bottom:
                break

            # Draw the line number right justified at the y position of the line.
            if block.isVisible():
                numberText = str(line_count)
                if block == current_block:
                    painter.setFont(self.boldFont)
                    leftPosition = self.width() - (self.boldMetrics.width(numberText) + self.MARGIN)
                    topPosition = position.y() + self.boldMetrics.ascent() + self.boldMetrics.descent() - 2
                    painter.drawText(leftPosition, topPosition, numberText)
                else:
                    painter.setFont(self.normalFont)
                    leftPosition = self.width() - (self.normalMetrics.width(numberText) + self.MARGIN)
                    topPosition = position.y() + self.normalMetrics.ascent() + self.normalMetrics.descent() - 2
                    painter.drawText(leftPosition, topPosition, numberText)
            
            block = block.next()

        painter.end()
        QtGui.QWidget.paintEvent(self, event)

class BookmarkSideBarAddon(QtGui.QWidget, SideBarWidgetAddon):
    ALIGNMENT = QtCore.Qt.AlignLeft
    
    @pmxConfigPorperty(default = False)
    def showBookmarks(self, value):
        self.setVisible(value)
    
    
    def __init__(self, parent):
        QtGui.QWidget.__init__(self, parent)
        self.bookmarkflagImage = resources.getImage("bookmarkflag")
        self.setFixedWidth(self.bookmarkflagImage.width())
        self.setObjectName(self.__class__.__name__)
        
    def initialize(self, editor):
        SideBarWidgetAddon.initialize(self, editor)
        self.background = self.editor.colours['gutter']
        self.foreground = self.editor.colours['gutterForeground']
        self.editor.themeChanged.connect(self.updateColours)
        
    def updateColours(self):
        self.background = self.editor.colours['gutter']
        self.foreground = self.editor.colours['gutterForeground']
        self.repaint(self.rect())

    @classmethod
    def contributeToMainMenu(cls):
        def on_actionShowBookmarks_toggled(editor, checked):
            instance = editor.findChild(cls, cls.__name__)
            if instance is not None:
                instance.setVisible(checked)

        def on_actionShowBookmarks_testChecked(editor):
            instance = editor.findChild(cls, cls.__name__)
            return instance is not None and instance.isVisible()
            
        baseMenu = ("view", cls.ALIGNMENT == QtCore.Qt.AlignRight and "Right Gutter" or "Left Gutter")
        menuEntry = {
            'name': 'bookmarks',
            'text': "Bookmarks",
            'callback': on_actionShowBookmarks_toggled,
            'shortcut': 'Alt+F10',
            'checkable': True,
            'testChecked': on_actionShowBookmarks_testChecked }
        return { baseMenu: menuEntry} 

    def paintEvent(self, event):
        font_metrics = QtGui.QFontMetrics(self.editor.font())
        page_bottom = self.editor.viewport().height()
       
        painter = QtGui.QPainter(self)
        painter.fillRect(self.rect(), self.background)

        block = self.editor.firstVisibleBlock()
        viewport_offset = self.editor.contentOffset()
        
        while block.isValid():
            # The top left position of the block in the document
            position = self.editor.blockBoundingGeometry(block).topLeft() + viewport_offset
            # Check if the position of the block is out side of the visible area
            if position.y() > page_bottom:
                break

            # Draw the line number right justified at the y position of the line.
            if block.isVisible() and block in self.editor.bookmarkListModel:
                painter.drawPixmap(0,
                    round(position.y()) + font_metrics.ascent() + font_metrics.descent() - self.bookmarkflagImage.height(),
                    self.bookmarkflagImage)

            block = block.next()

        painter.end()
        QtGui.QWidget.paintEvent(self, event)
        
    def mousePressEvent(self, event):
        block = self.translatePosition(event.pos())
        self.editor.toggleBookmark(block)
        self.repaint(self.rect())
            
class FoldingSideBarAddon(QtGui.QWidget, SideBarWidgetAddon):
    ALIGNMENT = QtCore.Qt.AlignLeft
    
    @pmxConfigPorperty(default = True)
    def showFolding(self, value):
        self.setVisible(value)
    

    def __init__(self, parent):
        QtGui.QWidget.__init__(self, parent)
        self.foldingcollapsedImage = resources.getImage("foldingcollapsed")
        self.foldingtopImage = resources.getImage("foldingtop")
        self.foldingbottomImage = resources.getImage("foldingbottom")
        self.setFixedWidth(self.foldingbottomImage.width())
        self.setObjectName(self.__class__.__name__)

    def initialize(self, editor):
        SideBarWidgetAddon.initialize(self, editor)
        self.background = self.editor.colours['gutter'] if 'gutter' in self.editor.colours else self.editor.colours['background']
        self.editor.themeChanged.connect(self.updateColours)
        
    def updateColours(self):
        self.background = self.editor.colours['gutter'] if 'gutter' in self.editor.colours else self.editor.colours['background']
        self.repaint(self.rect())
    
    @classmethod
    def contributeToMainMenu(cls):
        def on_actionShowFoldings_toggled(editor, checked):
            instance = editor.findChild(cls, cls.__name__)
            if instance is not None:
                instance.setVisible(checked)

        def on_actionShowFoldings_testChecked(editor):
            instance = editor.findChild(cls, cls.__name__)
            return instance is not None and instance.isVisible()
            
        baseMenu = ("view", cls.ALIGNMENT == QtCore.Qt.AlignRight and "Right Gutter" or "Left Gutter")
        menuEntry = {
            'name': 'foldings',
            'text': 'Foldings',
            'callback': on_actionShowFoldings_toggled,
            'shortcut': 'Shift+F10',
            'checkable': True,
            'testChecked': on_actionShowFoldings_testChecked }
        return {baseMenu: menuEntry} 

    def paintEvent(self, event):
        font_metrics = QtGui.QFontMetrics(self.editor.font())
        page_bottom = self.editor.viewport().height()
       
        painter = QtGui.QPainter(self)
        painter.fillRect(self.rect(), self.background)

        block = self.editor.firstVisibleBlock()
        viewport_offset = self.editor.contentOffset()
        
        while block.isValid():
            # The top left position of the block in the document
            position = self.editor.blockBoundingGeometry(block).topLeft() + viewport_offset
            # Check if the position of the block is out side of the visible area
            if position.y() > page_bottom:
                break

            # Draw the line number right justified at the y position of the line.
            if block.isVisible():
                userData = block.userData()
    
                mark = self.editor.folding.getFoldingMark(block)
                if self.editor.folding.isStart(mark):
                    if userData.folded:
                        painter.drawPixmap(0,
                            round(position.y()) + font_metrics.ascent() + font_metrics.descent() - self.foldingcollapsedImage.height(),
                            self.foldingcollapsedImage)
                    else:
                        painter.drawPixmap(0,
                            round(position.y()) + font_metrics.ascent() + font_metrics.descent() - self.foldingtopImage.height(),
                            self.foldingtopImage)
                elif self.editor.folding.isStop(mark):
                    painter.drawPixmap(0,
                        round(position.y()) + font_metrics.ascent() + font_metrics.descent() - self.foldingbottomImage.height(),
                        self.foldingbottomImage)

            block = block.next()

        painter.end()
        QtGui.QWidget.paintEvent(self, event)
        
    def mousePressEvent(self, event):
        block = self.translatePosition(event.pos())
        if self.editor.folding.isFoldingMark(block):
            if self.editor.folding.isFolded(block):
                self.editor.codeFoldingUnfold(block)
            else:
                self.editor.codeFoldingFold(block)

class SelectionSideBarAddon(QtGui.QWidget, SideBarWidgetAddon):
    ALIGNMENT = QtCore.Qt.AlignRight
    
    @pmxConfigPorperty(default = False)
    def showSelection(self, value):
        self.setVisible(value)
    
    def __init__(self, parent):
        QtGui.QWidget.__init__(self, parent)
        self.setFixedWidth(10)
        self.setObjectName(self.__class__.__name__)
        
    def initialize(self, editor):
        SideBarWidgetAddon.initialize(self, editor)
        self.background = self.editor.colours['gutter'] if 'gutter' in self.editor.colours else self.editor.colours['background']
        self.editor.themeChanged.connect(self.updateColours)
        self.editor.extraSelectionChanged.connect(self.on_editor_extraSelectionChanged)
        
    def updateColours(self):
        self.background = self.editor.colours['gutter'] if 'gutter' in self.editor.colours else self.editor.colours['background']
        self.update()
    
    def on_editor_extraSelectionChanged(self):
        self.update()

    @classmethod
    def contributeToMainMenu(cls):
        def on_actionShowSelection_toggled(editor, checked):
            instance = editor.findChild(cls, cls.__name__)
            if instance is not None:
                instance.setVisible(checked)

        def on_actionShowSelection_testChecked(editor):
            instance = editor.findChild(cls, cls.__name__)
            return instance is not None and instance.isVisible()
            
        baseMenu = ("view", cls.ALIGNMENT == QtCore.Qt.AlignRight and "Right Gutter" or "Left Gutter")
        menuEntry = {
            'name': 'selection',
            'text': 'Selection',
            'callback': on_actionShowSelection_toggled,
            'shortcut': 'Shift+F10',
            'checkable': True,
            'testChecked': on_actionShowSelection_testChecked }
        return {baseMenu: menuEntry} 

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

        viewport_offset = self.editor.contentOffset()

        for extra in self.editor.searchExtraSelections("selection"):
            y = round(extra.cursor.block().blockNumber() * rectRelation)
            if rectRelation == lineHeight:
                y += viewport_offset.y()
            painter.fillRect(0, y, 10, rectHeight, self.editor.colours['selection'])

        painter.end()
        QtGui.QWidget.paintEvent(self, event)
        
    def mousePressEvent(self, event):
        block = self.translatePosition(event.pos())
        print block
