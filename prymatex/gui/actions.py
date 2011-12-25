#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui

from prymatex import resources
from prymatex.gui import dialogs

class MainWindowActions(object):
    
    splitTabWidget = None #Overriden in GUI Setup
    
    def setupMenu(self):
        #Recent files
        self.actionFullscreen.setChecked(self.windowState() == QtCore.Qt.WindowFullScreen)
        self.actionShowStatus.setChecked(self.statusBar().isVisible())
        self.actionShowMenus.setChecked(self.menuBar().isVisible())
        
        #Bundles Menu
        self.application.supportManager.appendMenuToBundleMenuGroup(self.menuBundles)

    def updateMenuForEditor(self, editor):
        #TODO: if editor is none set disabled accions
        if editor is None: return
        flags = editor.getFlags()
        #TODO: Desconectar señales para poder hacer el set, medio raro
        self.actionShowLineNumbers.setChecked(bool(flags & editor.ShowLineNumbers))
        self.actionShowFolding.setChecked(bool(flags & editor.ShowFolding))
        self.actionShowBookmarks.setChecked(bool(flags & editor.ShowBookmarks))
        self.actionShowTabsAndSpaces.setChecked(bool(flags & editor.ShowTabsAndSpaces))
        self.actionShowLineAndParagraphs.setChecked(bool(flags & editor.ShowLineAndParagraphs))
        self.actionWordWrap.setChecked(bool(flags & editor.WordWrap))
        
    #============================================================
    # About To Show Menus
    #============================================================
    def on_menuFile_aboutToShow(self):
        pass

    def on_menuRecentFiles_aboutToShow(self):
        self.menuRecentFiles.clear()
        for filePath in self.application.fileManager.fileHistory:
            actionText = "%s (%s)"% (self.application.fileManager.fileName(filePath), filePath)
            action = QtGui.QAction(actionText, self)
            receiver = lambda file = filePath: self.application.openFile(file)
            self.connect(action, QtCore.SIGNAL('triggered()'), receiver)
            self.menuRecentFiles.addAction(action)
        self.menuRecentFiles.addSeparator()
        self.menuRecentFiles.addAction(self.actionOpenAllRecentFiles)
        self.menuRecentFiles.addAction(self.actionRemoveAllRecentFiles)

    def on_menuEdit_aboutToShow(self):
        pass
    
    def on_menuView_aboutToShow(self):
        pass

    #============================================================
    # File Actions
    #============================================================
    @QtCore.pyqtSlot()
    def on_actionNewEditor_triggered(self):
        self.addEmptyEditor()

    @QtCore.pyqtSlot()
    def on_actionNewFileFromTemplate_triggered(self):
        filePath = self.newFromTemplateDialog.getNewFileFromTemplate()
        if filePath:
            self.application.openFile(filePath)
    
    @QtCore.pyqtSlot()
    def on_actionNewProject_triggered(self):
        self.newProjectDialog.getNewProject()

    @QtCore.pyqtSlot()
    def on_actionOpen_triggered(self):
        filePath = self.currentEditor().filePath if self.currentEditor() is not None else None
        files = dialogs.getOpenFiles(directory = self.application.fileManager.getDirectory(filePath))
        focus = len(files) == 1
        for filePath in files:
            editor = self.application.openFile(filePath, focus = focus)
    
    @QtCore.pyqtSlot()
    def on_actionOpenAllRecentFiles_triggered(self):
        for filePath in self.application.fileManager.fileHistory:
            self.application.openFile(filePath)

    @QtCore.pyqtSlot()
    def on_actionRemoveAllRecentFiles_triggered(self):
        self.application.fileManager.clearFileHistory()

    @QtCore.pyqtSlot()
    def on_actionSave_triggered(self):
        self.saveEditor()
        
    @QtCore.pyqtSlot()
    def on_actionSaveAs_triggered(self):
        self.saveEditor(saveAs = True)
        
    @QtCore.pyqtSlot()
    def on_actionSaveAll_triggered(self):
        for w in self.splitTabWidget.getAllWidgets():
            self.saveEditor(editor = w)

    @QtCore.pyqtSlot()
    def on_actionClose_triggered(self):
        self.closeEditor()

    @QtCore.pyqtSlot()
    def on_actionCloseAll_triggered(self):
        for w in self.splitTabWidget.getAllWidgets():
            self.closeEditor(editor = w)

    @QtCore.pyqtSlot()
    def on_actionCloseOthers_triggered(self):
        current = self.currentEditor()
        for w in self.splitTabWidget.getAllWidgets():
            if w is not current:
                self.closeEditor(editor = w)
    
    @QtCore.pyqtSlot()
    def on_actionQuit_triggered(self):
        QtGui.QApplication.quit()
    
    #============================================================
    # Edit Actions
    #============================================================
    @QtCore.pyqtSlot()
    def on_actionUndo_triggered(self):
        if self.currentEditor() is not None:
            self.currentEditor().undo()

    @QtCore.pyqtSlot()
    def on_actionRedo_triggered(self):
        if self.currentEditor() is not None:
            self.currentEditor().redo()
        
    @QtCore.pyqtSlot()
    def on_actionCopy_triggered(self):
        if self.currentEditor() is not None:
            self.currentEditor().copy()
    
    @QtCore.pyqtSlot()
    def on_actionCut_triggered(self):
        if self.currentEditor() is not None:
            self.currentEditor().cut()
        
    @QtCore.pyqtSlot()
    def on_actionPaste_triggered(self):
        if self.currentEditor() is not None:
            self.currentEditor().paste()

    @QtCore.pyqtSlot()
    def on_actionSelectWord_triggered(self):
        if self.currentEditor() is not None:
            self.currentEditor().select(0)
    
    @QtCore.pyqtSlot()
    def on_actionSelectLine_triggered(self):
        if self.currentEditor() is not None:
            self.currentEditor().select(1)
    
    @QtCore.pyqtSlot()
    def on_actionSelectParagraph_triggered(self):
        if self.currentEditor() is not None:
            self.currentEditor().select(2)
    
    @QtCore.pyqtSlot()
    def on_actionSelectEnclosingBrackets_triggered(self):
        if self.currentEditor() is not None:
            self.currentEditor().select(self.currentEditor().SelectEnclosingBrackets)
        
    @QtCore.pyqtSlot()
    def on_actionSelectCurrentScope_triggered(self):
        if self.currentEditor() is not None:
            self.currentEditor().select(self.currentEditor().SelectCurrentScope)
        
    @QtCore.pyqtSlot()
    def on_actionSelectAll_triggered(self):
        if self.currentEditor() is not None:
            self.currentEditor().select(3)

    @QtCore.pyqtSlot()
    def on_actionFind_triggered(self):
        self.statusBar().showIFind()

    @QtCore.pyqtSlot()
    def on_actionFindReplace_triggered(self):
        self.statusBar().showFindReplace()
        
    #============================================================
    # View Actions
    #============================================================
    @QtCore.pyqtSlot()
    def on_actionZoomIn_triggered(self):
        if self.currentEditor() is not None:
            self.currentEditor().zoomIn()
            
    @QtCore.pyqtSlot()
    def on_actionZoomOut_triggered(self):
        if self.currentEditor() is not None:
            self.currentEditor().zoomOut()

    @QtCore.pyqtSlot(bool)
    def on_actionShowBookmarks_toggled(self, checked):
        if self.currentEditor() is not None:
            if checked:
                flags = self.currentEditor().getFlags() | self.currentEditor().ShowBookmarks
            else:
                flags = self.currentEditor().getFlags() & ~self.currentEditor().ShowBookmarks
            self.currentEditor().setFlags(flags)
    
    @QtCore.pyqtSlot(bool)
    def on_actionShowLineNumbers_toggled(self, checked):
        if self.currentEditor() is not None:
            if checked:
                flags = self.currentEditor().getFlags() | self.currentEditor().ShowLineNumbers
            else:
                flags = self.currentEditor().getFlags() & ~self.currentEditor().ShowLineNumbers
            self.currentEditor().setFlags(flags)
        
    @QtCore.pyqtSlot(bool)
    def on_actionShowFolding_toggled(self, checked):
        if self.currentEditor() is not None:
            if checked:
                flags = self.currentEditor().getFlags() | self.currentEditor().ShowFolding
            else:
                flags = self.currentEditor().getFlags() & ~self.currentEditor().ShowFolding
            self.currentEditor().setFlags(flags)
    
    @QtCore.pyqtSlot(bool)
    def on_actionShowTabsAndSpaces_toggled(self, checked):
        if self.currentEditor() is not None:
            if checked:
                flags = self.currentEditor().getFlags() | self.currentEditor().ShowTabsAndSpaces
            else:
                flags = self.currentEditor().getFlags() & ~self.currentEditor().ShowTabsAndSpaces
            self.currentEditor().setFlags(flags)
    
    @QtCore.pyqtSlot(bool)
    def on_actionShowLineAndParagraphs_toggled(self, checked):
        if self.currentEditor() is not None:
            if checked:
                flags = self.currentEditor().getFlags() | self.currentEditor().ShowLineAndParagraphs
            else:
                flags = self.currentEditor().getFlags() & ~self.currentEditor().ShowLineAndParagraphs
            self.currentEditor().setFlags(flags)
            
    @QtCore.pyqtSlot(bool)
    def on_actionWordWrap_toggled(self, checked):
        if self.currentEditor() is not None:
            if checked:
                flags = self.currentEditor().getFlags() | self.currentEditor().WordWrap
            else:
                flags = self.currentEditor().getFlags() & ~self.currentEditor().WordWrap
            self.currentEditor().setFlags(flags)

    #============================================================
    # Text Actions
    #============================================================
    @QtCore.pyqtSlot()
    def on_actionConvertToUppercase_triggered(self):
        if self.currentEditor() is not None:
            self.currentEditor().convertText(self.currentEditor().ConvertToUppercase)
    
    @QtCore.pyqtSlot()
    def on_actionConvertToLowercase_triggered(self):
        if self.currentEditor() is not None:
            self.currentEditor().convertText(self.currentEditor().ConvertToLowercase)
        
    @QtCore.pyqtSlot()
    def on_actionConvertToTitlecase_triggered(self):
        if self.currentEditor() is not None:
            self.currentEditor().convertText(self.currentEditor().ConvertToTitlecase)
        
    @QtCore.pyqtSlot()
    def on_actionConvertToOppositeCase_triggered(self):
        if self.currentEditor() is not None:
            self.currentEditor().convertText(self.currentEditor().ConvertToOppositeCase)
        
    @QtCore.pyqtSlot()
    def on_actionConvertSpacesToTabs_triggered(self):
        if self.currentEditor() is not None:
            self.currentEditor().convertText(self.currentEditor().ConvertSpacesToTabs)
        
    @QtCore.pyqtSlot()
    def on_actionConvertTabToSpaces_triggered(self):
        if self.currentEditor() is not None:
            self.currentEditor().convertText(self.currentEditor().ConvertTabsToSpaces)

    @QtCore.pyqtSlot()
    def on_actionConvertTranspose_triggered(self):
        if self.currentEditor() is not None:
            self.currentEditor().convertText(self.currentEditor().ConvertTranspose)

    #Move Menu
    @QtCore.pyqtSlot()
    def on_actionMoveLineUp_triggered(self):
        if self.currentEditor() is not None:
            self.currentEditor().moveText(self.currentEditor().MoveLineUp)
    
    @QtCore.pyqtSlot()
    def on_actionMoveLineDown_triggered(self):
        if self.currentEditor() is not None:
            self.currentEditor().moveText(self.currentEditor().MoveLineDown)
            
    @QtCore.pyqtSlot()
    def on_actionMoveColumnLeft_triggered(self):
        if self.currentEditor() is not None:
            self.currentEditor().moveText(self.currentEditor().MoveColumnLeft)
            
    @QtCore.pyqtSlot()
    def on_actionMoveColumnRight_triggered(self):
        if self.currentEditor() is not None:
            self.currentEditor().moveText(self.currentEditor().MoveColumnRight)
    
    @QtCore.pyqtSlot()
    def on_actionExecute_triggered(self):
        self.currentEditor().executeCommand()

    @QtCore.pyqtSlot()
    def on_actionFilterThroughCommand_triggered(self):
        self.statusBar().showCommand()

    #============================================================
    # Navigation Actions
    #============================================================
    @QtCore.pyqtSlot()
    def on_actionToggleBookmark_triggered(self):
        self.currentEditor().toggleBookmark()

    @QtCore.pyqtSlot()
    def on_actionNextBookmark_triggered(self):
        self.currentEditor().bookmarkNext()

    @QtCore.pyqtSlot()
    def on_actionPreviousBookmark_triggered(self):
        self.currentEditor().bookmarkPrevious()
        
    @QtCore.pyqtSlot()
    def on_actionRemoveAllBookmarks_triggered(self):
        self.currentEditor().removeAllBookmarks()

    @QtCore.pyqtSlot()
    def on_actionNextTab_triggered(self):
        self.splitTabWidget.focusNextTab()

    @QtCore.pyqtSlot()
    def on_actionPreviousTab_triggered(self):
        self.splitTabWidget.focusPreviousTab()

    @QtCore.pyqtSlot()
    def on_actionSelectTab_triggered(self):
        """ 
        Shows select tab, and change to selected 
        """
        tabs = self.splitTabWidget.getAllWidgets()
        def tabsToDict(tabs):
            for tab in tabs:
                image = tab.tabIcon()
                if image is None: image = QtGui.QIcon()
                yield [ dict(title = tab.tabTitle(), image = image), dict(title = tab.filePath) ]
        index = self.tabSelectorDialog.select(tabsToDict(tabs))
        if index is not None:
            tab = tabs[index]
            self.splitTabWidget.setCurrentWidget(tab, focus = True)
        
    @QtCore.pyqtSlot()
    def on_actionGoToLine_triggered(self):
        self.statusBar().showGoToLine()
        
    @QtCore.pyqtSlot()
    def on_actionGoToSymbol_triggered(self):
        editor = self.currentEditor()
        blocks = editor.symbolListModel.blocks
        def symbolToDict(blocks):
            for block in blocks:
                userData = block.userData() 
                yield [dict(title = userData.symbol, image = resources.getIcon('codefunction'))]
        index = self.symbolSelectorDialog.select(symbolToDict(blocks))
        if index is not None:
            editor.goToBlock(blocks[index])
        
    @QtCore.pyqtSlot()
    def on_actionGoToBookmark_triggered(self):
        editor = self.currentEditor()
        blocks = editor.bookmarkListModel.blocks
        def bookmarkToDict(blocks):
            for block in blocks:
                yield [dict(title = block.text(), image = resources.getIcon('bookmarkflag'))]
        index = self.bookmarkSelectorDialog.select(bookmarkToDict(blocks))
        if index is not None:
            editor.goToBlock(blocks[index])
            
    #============================================================
    # Bundles Actions
    #============================================================
    @QtCore.pyqtSlot()
    def on_actionShowBundleEditor_triggered(self):
        #TODO: mejorar esto
        self.application.bundleEditor.execEditor()

    @QtCore.pyqtSlot()
    def on_actionEditCommands_triggered(self):
        #TODO: mejorar esto
        self.application.bundleEditor.execCommand()
    
    @QtCore.pyqtSlot()
    def on_actionEditLanguages_triggered(self):
        #TODO: mejorar esto
        self.application.bundleEditor.execLanguage()
    
    @QtCore.pyqtSlot()
    def on_actionEditSnippets_triggered(self):
        #TODO: mejorar esto
        self.application.bundleEditor.execSnippet()
        
    @QtCore.pyqtSlot()
    def on_actionSelectBundleItem_triggered(self):
        editor = self.currentEditor()
        scope = editor.getCurrentScope()
        items = self.application.supportManager.getActionItems(scope)
        def itemsToDict(items):
            for item in items:
                yield [dict(title = item.name, image = item.TYPE), dict(title = item.trigger)]
        index = self.bundleSelectorDialog.select(itemsToDict(items))
        if index is not None:
            self.currentEditor().insertBundleItem(items[index])
    
    #============================================================
    # Preferences Actions
    #============================================================
    @QtCore.pyqtSlot(bool)
    def on_actionShowMenus_toggled(self, checked):
        self.menuBar().setVisible(checked)
        
    @QtCore.pyqtSlot(bool)
    def on_actionShowStatus_toggled(self, checked):
        self.statusBar().setVisible(checked)
    
    @QtCore.pyqtSlot(bool)
    def on_actionFullscreen_toggled(self, checked):
        if checked:
            self.showFullScreen()
        else:
            self.showNormal()

    @QtCore.pyqtSlot()
    def on_actionSettings_triggered(self):
        self.application.configDialog.exec_()
            
    #============================================================
    # Help Actions
    #============================================================
    @QtCore.pyqtSlot()
    def on_actionAbout_Qt_triggered(self):
        QtGui.qApp.aboutQt()
        
    @QtCore.pyqtSlot()
    def on_actionAbout_this_application_triggered(self):
        QtGui.QMessageBox.information(self, self.trUtf8("About Prymatex"), 
                                self.trUtf8("<h3>Prymatex</h3>"
                                "<p>A general purpouse Text Editor</p>")
                                )
        
    @QtCore.pyqtSlot()
    def on_actionProjectHomepage_triggered(self):
        import webbrowser
        import prymatex
        url = getattr(prymatex, '__url__', "https://github.com/D3f0/prymatex")
        webbrowser.open(url)

    @QtCore.pyqtSlot()
    def on_actionTakeScreenshot_triggered(self):
        pxm = QtGui.QPixmap.grabWindow(self.winId())
        from datetime import datetime
        now = datetime.now()
        name = "%s.%s" % (now.strftime('sshot-%Y-%m-%d-%H_%M_%S'), 'png')
        pxm.save(name, format)
        