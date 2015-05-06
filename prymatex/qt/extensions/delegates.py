#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtCore, QtGui, QtWidgets

class HtmlItemDelegate(QtWidgets.QItemDelegate):
    def __init__(self, parentView):
        QtWidgets.QItemDelegate.__init__(self, parentView)
        self.document = QtGui.QTextDocument(self)
        self.document.setDocumentMargin(0)

    def drawDisplay(self, painter, option, rect, text):
        # Fix if not table
        if option.state & QtWidgets.QStyle.State_Selected:
            background = option.palette.color(QtGui.QPalette.Active, QtGui.QPalette.Highlight)
            color = option.palette.color(QtGui.QPalette.Active, QtGui.QPalette.HighlightedText)
            self.document.setDefaultStyleSheet("""{ background-color: %s;
                color: %s; }""" % (background.name(), color.name()))
        else:
            self.document.setDefaultStyleSheet("")
        
        doc = self.document
        doc.setDefaultFont(option.font)
        doc.setHtml(text)
        doc.setTextWidth(option.rect.width() - option.decorationSize.width())
        
        painter.save()
        painter.translate(QtCore.QPoint(rect.left(), option.rect.top()))
        ctx = QtGui.QAbstractTextDocumentLayout.PaintContext()
        ctx.palette = option.palette
        doc.documentLayout().draw(painter, ctx)
        painter.restore()

    def sizeHint(self, option, index):
        record = index.data()
        self.document.setHtml(record)
        self.document.setTextWidth(option.rect.width())
        return QtCore.QSize(self.document.idealWidth(), self.document.size().height())

class HtmlLinkItemDelegate(QtWidgets.QItemDelegate):
    linkActivated = QtCore.Signal(str)
    linkHovered = QtCore.Signal(str)  # to connect to a QStatusBar.showMessage slot

    def __init__(self, parentView):
        QtWidgets.QItemDelegate.__init__(self, parentView)
        assert isinstance(parentView, QtWidgets.QAbstractItemView), \
            "The first argument must be the view"

        # We need that to receive mouse move events in editorEvent
        parentView.setMouseTracking(True)

        # Revert the mouse cursor when the mouse isn't over 
        # an item but still on the view widget
        parentView.viewportEntered.connect(parentView.unsetCursor)

        # documents[0] will contain the document for the last hovered item
        # documents[1] will be used to draw ordinary (not hovered) items
        self.documents = []
        for i in range(2):
            self.documents.append(QtGui.QTextDocument(self))
            self.documents[i].setDocumentMargin(0)
        self.lastTextPos = QtCore.QPoint(0,0)

    def drawDisplay(self, painter, option, rect, text): 
        # Because the state tells only if the mouse is over the row
        # we have to check if it is over the item too
        mouseOver = option.state & QtWidgets.QStyle.State_MouseOver \
            and rect.contains(self.parent().viewport() \
                .mapFromGlobal(QtGui.QCursor.pos())) \
            and option.state & QtWidgets.QStyle.State_Enabled

        if mouseOver:
            # Use documents[0] and save the text position for editorEvent
            doc = self.documents[0]                
            self.lastTextPos = rect.topLeft()
            doc.setDefaultStyleSheet("")
        else:
            doc = self.documents[1]
            # Links are decorated by default, so disable it
            # when the mouse is not over the item
            doc.setDefaultStyleSheet("a {text-decoration: none}")

        doc.setDefaultFont(option.font)
        doc.setHtml(text)
        doc.setTextWidth(option.rect.width() - option.decorationSize.width())
        
        painter.save()
        painter.translate(QtCore.QPoint(rect.left(), option.rect.top()))
        ctx = QtGui.QAbstractTextDocumentLayout.PaintContext()
        ctx.palette = option.palette
        doc.documentLayout().draw(painter, ctx)
        painter.restore()

    def editorEvent(self, event, model, option, index):
        if event.type() not in [QtCore.QEvent.MouseMove, QtCore.QEvent.MouseButtonRelease] \
            or not (option.state & QtWidgets.QStyle.State_Enabled):
            return False                        
        # Get the link at the mouse position
        # (the explicit QPointF conversion is only needed for PyQt)
        pos = QtCore.QPointF(event.pos() - self.lastTextPos)
        anchor = self.documents[0].documentLayout().anchorAt(pos)
        if anchor == "":
            self.parent().unsetCursor()
        else:
            self.parent().setCursor(QtCore.Qt.PointingHandCursor)               
            if event.type() == QtCore.QEvent.MouseButtonRelease:
                self.linkActivated.emit(anchor)
                return True 
            else:
                self.linkHovered.emit(anchor)
        return False

    def sizeHint(self, option, index):
        # Use a QTextDocument to strip the tags
        doc = self.documents[1]
        html = index.data()
        doc.setHtml(html)
        doc.setTextWidth(option.rect.width())
        return QtCore.QSize(doc.idealWidth(), doc.size().height())
