# -*- coding: utf-8 -*-
from PyQt4.QtGui import QDialog, QMessageBox, QToolTip
from PyQt4.QtCore import SIGNAL, QProcess
from ui_filterthroughcommand import Ui_FilterThroughCommand
from prymatex.gui import PMXBaseGUIMixin
from prymatex.lib.i18n import ugettext as _
import logging

logger = logging.getLogger(__name__)

class PMXFilterDialog(QDialog, Ui_FilterThroughCommand, PMXBaseGUIMixin):
    def __init__(self, parent):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.connect(self, SIGNAL("accepted()"), self.accepted)
        self.connect(self, SIGNAL("rejected()"), self.rejected)

    def accepted (self):
        
        cmd = self.comboCommand.currentText()
        if not cmd:
            return
        if self.radioInputNone.isChecked():
            txt_input = None
        elif self.radioInputSelection.isChecked():
            txt_input = self.currentEditor.textCursor().selectedText()
        elif self.radioInputDocument.isChecked():
            txt_input = self.currentEditor.toPlainText()
        txt_input = txt_input and unicode(txt_input, 'utf-8') or ''
        logger.info(txt_input)
        self.proc = QProcess(self)
        self.proc.start(cmd)
        self.proc.waitForStarted()
        if txt_input:
            self.proc.write(txt_input)
            self.proc.closeWriteChannel()
        if not self.proc.waitForFinished(3000):
            logger.info("Output with errors while calling %s" % cmd)
            output = self.proc.readAllStandardError()
            #QMessageBox.warning(self, "Error", _(u"%s", output) )
        else:
            output = self.proc.readAllStandardOutput ()
        output = unicode(output.data(), 'utf-8')
        # Process Output
        if self.radioOutputDiscard.isChecked():
            return
        elif self.radioOutputSelection.isChecked():
            cursor = self.currentEditor.textCursor()
            cursor.beginEditBlock()
            cursor.clearSelection()
            cursor.insertText(output)
            cursor.endEditBlock()
        elif self.radioOutputDocument.isChecked():
            cursor = self.currentEditor.textCursor()
            cursor.beginEditBlock()
            self.currentEditor.setPlainText(ouput)
            #cursor.clearSelection()
            #cursor.setText(output)
            cursor.endEditBlock()
        elif self.radioOutputCreateNewDocument.isChecked():
            
            editor = self.mainWindow.tabWidgetEditors.appendEmptyTab()
            editor.setPlainText(output)
            
        elif self.radioOutputInsertSnippet.isChecked():
            pass
        elif self.radioOutputInsertText.isChecked():
            cursor = self.currentEditor.textCursor()
            cursor.beginEditBlock()
            cursor.insertText(output)
            cursor.endEditBlock()
        elif self.radioOutputShowAsHTML.isChecked():
            pass
        elif self.radioOutputShowToolTip.isChecked():
            point = self.currentEditor.cursorRect().bottomRight()
            point = self.mainWindow.mapToGlobal(point)
            logger.info("Mostrar como tooltip %s %s", point, output)
            
            QToolTip.showText(point, output, self.mainWindow)
            