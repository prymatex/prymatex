#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt import QtGui, QtCore

class HtmlItemDelegate(QtGui.QItemDelegate):

    def drawDisplay(self, painter, option, rect, text):
        doc = QtGui.QTextDocument(self)
        doc.setHtml(text)
        doc.setTextWidth(option.rect.width() - option.decorationSize.width())
        ctx = QtGui.QAbstractTextDocumentLayout.PaintContext()

        painter.save()
        
        painter.translate(QtCore.QPoint(rect.left(), option.rect.top()))
        dl = doc.documentLayout()
        dl.draw(painter, ctx)
        painter.restore()


    def sizeHint(self, option, index):
        model = index.model()
        record = model.data(index)
        doc = QtGui.QTextDocument(self)
        doc.setHtml(record)
        doc.setTextWidth(option.rect.width())
        return QtCore.QSize(doc.idealWidth(), doc.size().height())
