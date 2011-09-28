from PyQt4 import QtCore, QtGui

class MainWindowActions(object):
    def setupMenu(self):
        #Recent files
        self._update_file_history()
        
        #Bundles Menu
        self.application.supportManager.appendBundleMenuGroup(self.menuBundles)
        
        #Connects
        self.application.fileManager.fileHistoryChanged.connect(self._update_file_history)
    
    def on_menuFile_aboutToShow(self):
        self.actionSave.setEnabled(self.currentEditor.isModified())
        self.actionSave_All.setEnabled(any(map(lambda editor: editor.isModified(), self.splitTabWidget.getAllWidgets())))
        print "configurar menu file"
        
    def on_menuEdit_aboutToShow(self):
        print "configurar menu edit"
    
    def _update_file_history(self):
        menu = self.actionOpen_Recent.menu()
        if menu is None:
            menu = QtGui.QMenu(self)
            self.actionOpen_Recent.setMenu(menu)
        else:
            menu.clear()
        for file in self.application.fileManager.fileHistory:
            action = QtGui.QAction(file, self)
            receiver = lambda file = QtCore.QFile(file): self.openFile(file)
            self.connect(action, QtCore.SIGNAL('triggered()'), receiver)
            menu.addAction(action)
            
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
    def on_actionProjectHomePage_triggered(self):
        import webbrowser
        webbrowser.open(qApp.instance().projectUrl)
        
    @QtCore.pyqtSlot()
    def on_actionSave_triggered(self):
        self.saveFile()
        
    @QtCore.pyqtSlot()
    def on_actionSave_As_triggered(self):
        self.saveFile(saveAs = True)
        
    @QtCore.pyqtSlot()
    def on_actionSave_All_triggered(self):
        for w in self.splitTabWidget.getAllWidgets():
            self.saveFile(editor = w)

    @QtCore.pyqtSlot()
    def on_actionTake_Screenshot_triggered(self):
        pxm = QPixmap.grabWindow(self.winId())
        from datetime import datetime
        now = datetime.now()
        name = "%s.%s" % (now.strftime('sshot-%Y-%m-%d-%H_%M_%S'), 'png')
        pxm.save(name, format)
    
    @QtCore.pyqtSlot()
    def on_actionZoom_In_triggered(self):
        self.currentEditor.zoomIn()
            
    @QtCore.pyqtSlot()
    def on_actionZoom_Out_triggered(self):
        self.currentEditor.zoomOut()
        
    @QtCore.pyqtSlot()
    def on_actionFilter_Through_Command_triggered(self):
        self.dialogFilter.exec_()
        
    @QtCore.pyqtSlot()
    def on_actionClose_Others_triggered(self):
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
    def on_actionMove_Tab_Left_triggered(self):
        self.tabWidget.moveTabLeft()
        
    @QtCore.pyqtSlot()
    def on_actionMove_Tab_Right_triggered(self):
        self.tabWidget.moveTabRight()

    @QtCore.pyqtSlot()
    def on_actionSelect_Bundle_Item_triggered(self):
        editor = self.currentEditor
        scope = editor.getCurrentScope()
        items = self.application.supportManager.getActionItems(scope)
        item = self.bundleItemSelector.select(items)
        if item is not None:
            self.currentEditor.insertBundleItem(item)

    @QtCore.pyqtSlot()
    def on_actionNew_triggered(self):
        editor = self.application.getEditorInstance(parent = self)
        self.splitTabWidget.addTab(editor)
        
    @QtCore.pyqtSlot()
    def on_actionClose_triggered(self):
        index = self.tabWidget.currentIndex()
        self.tabWidget.closeTab(index)
        if self.tabWidget.count():
            self.tabWidget.currentWidget().setFocus(Qt.TabFocusReason)

    @QtCore.pyqtSlot()
    def on_actionQuit_triggered(self):
        QApplication.quit()
    
    
    @QtCore.pyqtSlot()
    def on_actionNext_Tab_triggered(self):
        self.tabWidget.focusNextTab()
    

    @QtCore.pyqtSlot()
    def on_actionPrevious_Tab_triggered(self):
        self.tabWidget.focusPrevTab()

    @QtCore.pyqtSlot(bool)
    def on_actionFullscreen_toggled(self, check):
        if not check and self.isFullScreen():
            self.showNormal()
        elif check:
            self.showFullScreen()
    
    @QtCore.pyqtSlot(bool)
    def on_actionShow_Menus_toggled(self, state):
        menubar = self.menuBar()
        if state:
            menubar.show()
        else:
            menubar.hide()
        
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
    def on_actionShow_Bundle_Editor_triggered(self):
        #TODO: mejorar esto
        self.application.bundleEditor.exec_()
        
    #===========================================================================
    # Dumb code :/
    #===========================================================================
    @QtCore.pyqtSlot()
    def on_actionPreferences_triggered(self):
        self.application.configDialog.exec_()
    
        
    @QtCore.pyqtSlot()
    def on_actionPaste_As_New_triggered(self):
        text = qApp.instance().clipboard().text()
        if text:
            editor = self.addEmptyEditor()
            editor.appendPlainText(text)
        else:
            self.mainWindow.statusBar().showMessage(self.trUtf8("Nothing to paste."))
        
    @QtCore.pyqtSlot()
    def on_actionGo_To_Line_triggered(self):
        self.currentEditor.goToLine()
        
    @QtCore.pyqtSlot()
    def on_actionGo_To_File_triggered(self):
        '''
        Triggers 
        '''
        self.tabWidget.chooseFileDlg.exec_()
        
    @QtCore.pyqtSlot()
    def on_actionFind_triggered(self):
        print "MainWindow::find"
        self.currentEditor.showFindWidget()
        
    @QtCore.pyqtSlot()
    def on_actionFind_Replace_triggered(self):
        print "MainWindow::replace"
        self.currentEditor.showReplaceWidget()

    #===========================================================
    # Templates
    #===========================================================
    def newFileFromTemplate(self, path):
        self.openFile(path, auto_focus=True)
        
    @QtCore.pyqtSlot()
    def on_actionNew_from_template_triggered(self):
        self.dialogNewFromTemplate.exec_()
    
    #============================================================
    # Bookmarks
    #============================================================
    @QtCore.pyqtSlot()
    def on_actionToggle_Bookmark_triggered(self):
        self.currentEditor.toggleBookmark(editor.textCursor().block().blockNumber() + 1)

    @QtCore.pyqtSlot()
    def on_actionNext_Bookmark_triggered(self):
        self.currentEditor.bookmarkNext(editor.textCursor().block().blockNumber() + 1)

    @QtCore.pyqtSlot()
    def on_actionPrevious_Bookmark_triggered(self):
        self.currentEditor.bookmarkPrevious(editor.textCursor().block().blockNumber() + 1)
        
    @QtCore.pyqtSlot()
    def on_actionRemove_All_Bookmarks_triggered(self):
        self.currentEditor.removeBookmarks()