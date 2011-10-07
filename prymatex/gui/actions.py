from PyQt4 import QtCore, QtGui

class MainWindowActions(object):
    def setupMenu(self):
        #Recent files
        self.actionFullscreen.setChecked(self.windowState() == QtCore.Qt.WindowFullScreen)
        self.actionShowStatus.setChecked(self.statusBar().isVisible())
        self.actionShowMenus.setChecked(self.menuBar().isVisible())
        
        #Bundles Menu
        self.application.supportManager.appendBundleMenuGroup(self.menuBundles)

    #============================================================
    # About To Show Menus
    #============================================================
    def on_menuFile_aboutToShow(self):
        self.actionSave.setEnabled(self.currentEditor is not None and self.currentEditor.isModified())
        self.actionSaveAll.setEnabled(any(map(lambda editor: editor.isModified(), self.splitTabWidget.getAllWidgets())))
        self.menuRecentFiles.menuAction().setEnabled(bool(self.application.fileManager.fileHistory))
        
    def on_menuFile_aboutToShow(self):
        self.actionSave.setEnabled(self.currentEditor is not None and self.currentEditor.isModified())
        self.actionSaveAll.setEnabled(any(map(lambda editor: editor.isModified(), self.splitTabWidget.getAllWidgets())))
    
    def on_menuRecentFiles_aboutToShow(self):
        self.menuRecentFiles.clear()
        for file in self.application.fileManager.fileHistory:
            action = QtGui.QAction(file, self)
            receiver = lambda file = QtCore.QFileInfo(file): self.openFile(file)
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
    def on_actionNew_triggered(self):
        self.addEmptyEditor()

    @QtCore.pyqtSlot()
    def on_actionNewFromTemplate_triggered(self):
        path = self.dialogNewFromTemplate.getNewFileFromTemplate()
        if path:
            self.openFile(QtCore.QFileInfo(path))

    @QtCore.pyqtSlot()
    def on_actionOpen_triggered(self):
        fileInfo = self.currentEditor.fileInfo if self.currentEditor is not None else None
        files = self.application.fileManager.getOpenFiles(fileInfo = fileInfo)
        for file in files:
            editor = self.openFile(file)
            self.setCurrentEditor(editor)
    
    def on_actionOpenAllRecentFiles_triggered(self):
        for file in self.application.fileManager.fileHistory:
            fileInfo = QtCore.QFileInfo(file)
            self.openFile(fileInfo)

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
        current = self.currentEditor
        for w in self.splitTabWidget.getAllWidgets():
            if w is not current:
                self.closeEditor(editor = w)
    
    @QtCore.pyqtSlot()
    def on_actionQuit_triggered(self):
        QApplication.quit()
    
    #============================================================
    # Edit Actions
    #============================================================
    @QtCore.pyqtSlot()
    def on_actionUndo_triggered(self):
        if self.currentEditor is not None:
            self.currentEditor.undo()
        
    @QtCore.pyqtSlot()
    def on_actionRedo_triggered(self):
        if self.currentEditor is not None:
            self.currentEditor.redo()
        
    @QtCore.pyqtSlot()
    def on_actionCopy_triggered(self):
        if self.currentEditor is not None:
            self.currentEditor.copy()
    
    @QtCore.pyqtSlot()
    def on_actionCut_triggered(self):
        if self.currentEditor is not None:
            self.currentEditor.cut()
        
    @QtCore.pyqtSlot()
    def on_actionPaste_triggered(self):
        if self.currentEditor is not None:
            self.currentEditor.paste()

    @QtCore.pyqtSlot()
    def on_actionSelectWord_triggered(self):
        if self.currentEditor is not None:
            self.currentEditor.select(0)
    
    @QtCore.pyqtSlot()
    def on_actionSelectLine_triggered(self):
        if self.currentEditor is not None:
            self.currentEditor.select(1)
    
    @QtCore.pyqtSlot()
    def on_actionSelectParagraph_triggered(self):
        if self.currentEditor is not None:
            self.currentEditor.select(2)
    
    @QtCore.pyqtSlot()
    def on_actionSelectEnclosingBrackets_triggered(self):
        pass
        
    @QtCore.pyqtSlot()
    def on_actionSelectCurrentScope_triggered(self):
        pass
        
    @QtCore.pyqtSlot()
    def on_actionSelectAll_triggered(self):
        if self.currentEditor is not None:
            self.currentEditor.select(3)

    @QtCore.pyqtSlot()
    def on_actionFind_triggered(self):
        self.statusBar().showFind()

    @QtCore.pyqtSlot()
    def on_actionFindReplace_triggered(self):
        self.statusBar().showFindReplace()
        
    #============================================================
    # View Actions
    #============================================================
    @QtCore.pyqtSlot()
    def on_actionZoomIn_triggered(self):
        if self.currentEditor is not None:
            self.currentEditor.zoomIn()
            
    @QtCore.pyqtSlot()
    def on_actionZoomOut_triggered(self):
        if self.currentEditor is not None:
            self.currentEditor.zoomOut()

    @QtCore.pyqtSlot()
    def on_actionShowFolding_triggered(self):
        self.statusBar().showMessage("actionShowFolding")
    
    @QtCore.pyqtSlot()
    def on_actionShowBookmarks_triggered(self):
        self.statusBar().showMessage("actionShowBookmarks")
    
    @QtCore.pyqtSlot()
    def on_actionShowLineNumbers_triggered(self):
        self.statusBar().showMessage("actionShowLineNumbers")

    #============================================================
    # Text Actions
    #============================================================
    @QtCore.pyqtSlot()
    def on_actionToUppercase_triggered(self):
        self.statusBar().showMessage("actionToUppercase")
    
    @QtCore.pyqtSlot()
    def on_actionToLowercase_triggered(self):
        self.statusBar().showMessage("actionToLowercase")
        
    @QtCore.pyqtSlot()
    def on_actionToTitlecase_triggered(self):
        self.statusBar().showMessage("actionToTitlecase")
        
    @QtCore.pyqtSlot()
    def on_actionToOppositeCase_triggered(self):
        self.statusBar().showMessage("actionToOppositeCase")
        
    @QtCore.pyqtSlot()
    def on_actionSpacesToTabs_triggered(self):
        self.statusBar().showMessage("actionSpacesToTabs")
        
    @QtCore.pyqtSlot()
    def on_actionTabToSpaces_triggered(self):
        self.statusBar().showMessage("actionTabToSpaces")

    @QtCore.pyqtSlot()
    def on_actionTranspose_triggered(self):
        self.statusBar().showMessage("actionTranspose")

    @QtCore.pyqtSlot()
    def on_actionExecute_triggered(self):
        self.currentEditor.executeCommand()

    @QtCore.pyqtSlot()
    def on_actionFilterThroughCommand_triggered(self):
        self.statusBar().showCommand()

    #============================================================
    # Navigation Actions
    #============================================================
    @QtCore.pyqtSlot()
    def on_actionToggleBookmark_triggered(self):
        self.currentEditor.toggleBookmark()

    @QtCore.pyqtSlot()
    def on_actionNextBookmark_triggered(self):
        self.currentEditor.bookmarkNext()

    @QtCore.pyqtSlot()
    def on_actionPreviousBookmark_triggered(self):
        self.currentEditor.bookmarkPrevious()
        
    @QtCore.pyqtSlot()
    def on_actionRemoveAllBookmarks_triggered(self):
        self.currentEditor.removeAllBookmarks()

    @QtCore.pyqtSlot()
    def on_actionNextTab_triggered(self):
        self.tabWidget.focusNextTab()

    @QtCore.pyqtSlot()
    def on_actionPreviousTab_triggered(self):
        self.tabWidget.focusPrevTab()

    #============================================================
    # Bundles Actions
    #============================================================
    @QtCore.pyqtSlot()
    def on_actionShowBundleEditor_triggered(self):
        #TODO: mejorar esto
        self.application.bundleEditor.exec_()

    @QtCore.pyqtSlot()
    def on_actionSelectBundleItem_triggered(self):
        editor = self.currentEditor
        scope = editor.getCurrentScope()
        items = self.application.supportManager.getActionItems(scope)
        item = self.bundleItemSelector.select(items)
        if item is not None:
            self.currentEditor.insertBundleItem(item)
    
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
        qApp.aboutQt()
        
    @QtCore.pyqtSlot()
    def on_actionAbout_this_application_triggered(self):
        QMessageBox.information(self, self.trUtf8("About Prymatex"), 
                                self.trUtf8("<h3>Prymatex</h3>"
                                "<p>A general purpouse Text Editor</p>")
                                )
        
    @QtCore.pyqtSlot()
    def on_actionProjectHomepage_triggered(self):
        import webbrowser
        webbrowser.open(qApp.instance().projectUrl)

    @QtCore.pyqtSlot()
    def on_actionTakeScreenshot_triggered(self):
        pxm = QPixmap.grabWindow(self.winId())
        from datetime import datetime
        now = datetime.now()
        name = "%s.%s" % (now.strftime('sshot-%Y-%m-%d-%H_%M_%S'), 'png')
        pxm.save(name, format)
        
