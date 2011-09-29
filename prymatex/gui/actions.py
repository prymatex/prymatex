from PyQt4 import QtCore, QtGui

class MainWindowActions(object):
    def setupMenu(self):
        #Recent files
        self._update_file_history()
        self.actionFullscreen.setChecked(self.windowState() == QtCore.Qt.WindowFullScreen)
        self.actionShowStatus.setChecked(self.statusBar().isVisible())
        self.actionShowMenus.setChecked(self.menuBar().isVisible())
        
        #Bundles Menu
        self.application.supportManager.appendBundleMenuGroup(self.menuBundles)
        
        #Connects
        self.application.fileManager.fileHistoryChanged.connect(self._update_file_history)
    
    #============================================================
    # About To Show Menus
    #============================================================
    def on_menuFile_aboutToShow(self):
        self.actionSave.setEnabled(self.currentEditor.isModified())
        self.actionSaveAll.setEnabled(any(map(lambda editor: editor.isModified(), self.splitTabWidget.getAllWidgets())))
        print "configurar menu file"
        
    def on_menuEdit_aboutToShow(self):
        print "configurar menu edit"
    
    def _update_file_history(self):
        menu = self.actionOpenRecent.menu()
        if menu is None:
            menu = QtGui.QMenu(self)
            self.actionOpenRecent.setMenu(menu)
        else:
            menu.clear()
        for file in self.application.fileManager.fileHistory:
            action = QtGui.QAction(file, self)
            receiver = lambda file = QtCore.QFileInfo(file): self.openFile(file)
            self.connect(action, QtCore.SIGNAL('triggered()'), receiver)
            menu.addAction(action)
    
    #============================================================
    # File Actions
    #============================================================
    @QtCore.pyqtSlot()
    def on_actionNew_triggered(self):
        editor = self.application.getEditorInstance(parent = self)
        self.splitTabWidget.addTab(editor)

    @QtCore.pyqtSlot()
    def on_actionNewFromTemplate_triggered(self):
        path = self.dialogNewFromTemplate.getNewFileFromTemplate()
        if path:
            self.openFile(QtCore.QFileInfo(path))

    @QtCore.pyqtSlot()
    def on_actionOpen_triggered(self):
        '''
        Opens one or more files
        '''
        #TODO: El directory puede ser dependiente del current editor o del file manager
        files = self.application.fileManager.getOpenFiles()
        for file in files:
            self.openFile(file)
    
    @QtCore.pyqtSlot()
    def on_actionSave_triggered(self):
        self.saveFile()
        
    @QtCore.pyqtSlot()
    def on_actionSaveAs_triggered(self):
        self.saveFile(saveAs = True)
        
    @QtCore.pyqtSlot()
    def on_actionSaveAll_triggered(self):
        for w in self.splitTabWidget.getAllWidgets():
            self.saveFile(editor = w)

    @QtCore.pyqtSlot()
    def on_actionClose_triggered(self):
        index = self.tabWidget.currentIndex()
        self.tabWidget.closeTab(index)
        if self.tabWidget.count():
            self.tabWidget.currentWidget().setFocus(Qt.TabFocusReason)

    @QtCore.pyqtSlot()
    def on_actionCloseAll_triggered(self):
        index = self.tabWidget.currentIndex()
        self.tabWidget.closeTab(index)
        if self.tabWidget.count():
            self.tabWidget.currentWidget().setFocus(Qt.TabFocusReason)

    @QtCore.pyqtSlot()
    def on_actionCloseOthers_triggered(self):
        count = self.tabWidgetEditors.count()
        index = self.tabWidgetEditors.currentIndex()
        widgets = []
        
        for i in range(0, index) + range(index+1, count):
            widgets.append(self.tabWidgetEditors.widget(i))
        for w in widgets:
            i = self.tabWidgetEditors.indexOf(w)
            if not self.tabWidgetEditors.closeTab(i):
                return
    
    @QtCore.pyqtSlot()
    def on_actionQuit_triggered(self):
        QApplication.quit()
    
    #============================================================
    # Edit Actions
    #============================================================
    @QtCore.pyqtSlot()
    def on_actionUndo_triggered(self):
        self.statusBar().showMessage("actionUndo")
        
    @QtCore.pyqtSlot()
    def on_actionRedo_triggered(self):
        self.statusBar().showMessage("actionRedo")
        
    @QtCore.pyqtSlot()
    def on_actionCopy_triggered(self):
        self.statusBar().showMessage("actionCopy")
    
    @QtCore.pyqtSlot()
    def on_actionCut_triggered(self):
        self.statusBar().showMessage("actionCut")
        
    @QtCore.pyqtSlot()
    def on_actionPaste_triggered(self):
        self.statusBar().showMessage("actionPaste")

    @QtCore.pyqtSlot()
    def on_actionFind_triggered(self):
        self.currentEditor.showFindWidget()

    #============================================================
    # View Actions
    #============================================================
    @QtCore.pyqtSlot()
    def on_actionZoomIn_triggered(self):
        self.currentEditor.zoomIn()
            
    @QtCore.pyqtSlot()
    def on_actionZoomOut_triggered(self):
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
        self.statusBar().showMessage("actionExecute")

    @QtCore.pyqtSlot()
    def on_actionFilterThroughCommand_triggered(self):
        self.dialogFilter.exec_()

    #============================================================
    # Navigation Actions
    #============================================================
    @QtCore.pyqtSlot()
    def on_actionToggleBookmark_triggered(self):
        self.currentEditor.toggleBookmark(editor.textCursor().block().blockNumber() + 1)

    @QtCore.pyqtSlot()
    def on_actionNextBookmark_triggered(self):
        self.currentEditor.bookmarkNext(editor.textCursor().block().blockNumber() + 1)

    @QtCore.pyqtSlot()
    def on_actionPreviousBookmark_triggered(self):
        self.currentEditor.bookmarkPrevious(editor.textCursor().block().blockNumber() + 1)
        
    @QtCore.pyqtSlot()
    def on_actionRemoveAllBookmarks_triggered(self):
        self.currentEditor.removeBookmarks()

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

    #===========================================================================
    # Dumb code :/
    #===========================================================================
    @QtCore.pyqtSlot()
    def on_actionFindReplace_triggered(self):
        print "MainWindow::replace"
        self.currentEditor.showReplaceWidget()
