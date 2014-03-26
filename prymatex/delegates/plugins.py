#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prymatex.qt.extensions import HtmlItemDelegate

class PluginItemDelegate(HtmlItemDelegate):

    def drawDisplay(self, painter, option, rect, text):
        return HtmlItemDelegate.drawDecoration(self, painter, option, rect, text)

    def drawDecoration(self, painter, option, rect, pixmap):
        return HtmlItemDelegate.drawDecoration(self, painter, option, rect, pixmap)

    def sizeHint(self, option, index):
        return HtmlItemDelegate.drawDecoration(self, option, index)
