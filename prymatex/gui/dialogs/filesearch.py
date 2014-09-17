#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Based on Ninja IDE https://github.com/ninja-ide/ninja-ide/blob/master/ninja_ide/gui/misc/find_in_files.py
import os
try:
    import queue
except ImportError:
    import Queue as queue

from prymatex.qt import QtCore, QtGui, QtWidgets

from prymatex.ui.dialogs.search import Ui_SearchDialog
from functools import reduce

class FileSearchThread(QtCore.QThread):
    foundPattern = QtCore.Signal(str, list)
    
    def __init__(self, application, parent = None):
        QtCore.QThread.__init__(self, parent)
        self.application = application
        
    def searchInFiles(self, directories, filePattern, searchPattern, recursive, by_phrase):
        self._cancel = False
        self.recursive = recursive
        self.searchPattern = searchPattern
        self.filePatterns = filePattern.split(";")
        self.by_phrase = by_phrase
        self.queue = queue.Queue()
        for directory in directories:
            self.queue.put(directory)
        #Start!
        self.start()

    def run(self):
        while not self._cancel and not self.queue.empty():
            currentDirectory = self.queue.get()
            
            #Collect all sub dirs!
            currentFiles = []
            entries = self.application.fileManager.listDirectory(currentDirectory, absolute = True, filePatterns = self.filePatterns)
            for enrty in entries:
                if os.path.isfile(enrty):
                    currentFiles.append(enrty)
                elif os.path.isdir(enrty) and self.recursive:
                    self.queue.put(enrty)
            
            #process all files in current dir!
            for one_file in currentFiles:
                self._grep_file(one_file)

    def _grep_file(self, file_path):
        if not self.by_phrase:
            with open(file_path, 'r') as f:
                #TODO: Ver mejor el tema de unicode 
                content = f.read().decode("utf-8")
            words = [word for word in self.searchPattern.split('|')]
            words.insert(0, True)

            def check_whole_words(result, word):
                return result and content.find(word) != -1
            if not reduce(check_whole_words, words):
                return

        file_object = QtCore.QFile(file_path)
        if not file_object.open(QtCore.QFile.ReadOnly):
            return

        stream = QtCore.QTextStream(file_object)
        lines = []
        line_index = 1
        line = stream.readLine()
        while not self._cancel:
            column = line.find(self.searchPattern)
            if column != -1:
                lines.append((line_index, line))
            #take the next line!
            line = stream.readLine()
            if stream.atEnd():
                break
            line_index += 1
        #emit a signal!
        self.foundPattern.emit(file_path, lines)

    def cancel(self):
        self._cancel = True

class PMXFileSearchDialog(QtWidgets.QDialog, Ui_SearchDialog):
    def __init__(self, model, parent = None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.application = QtGui.QApplication.instance()
        self.model = model
        self.fileSearchThread = FileSearchThread(self.application, self)
        self.fileSearchThread.foundPattern.connect(self.on_fileSearchThread_foundPattern)
        
        self.comboBoxContainingText.lineEdit().returnPressed.connect(self.buttonSearch.click)
        
    def on_fileSearchThread_foundPattern(self, filePath, lines):
        if lines:
            self.model.addFileFound(filePath, lines)
        
    def on_buttonCancel_pressed(self):
        #FIXME: solo si esta corriendo
        self.fileSearchThread.cancel()
        self.reject()
        
    def on_buttonSearch_pressed(self):
        self.model.clear()
        searchPattern = self.comboBoxContainingText.lineEdit().text()
        filters = self.comboBoxFilePatterns.lineEdit().text()
        recursive = True
        byPhrase = True
        #self.comboBoxWorkingSet
        #self.searchInFiles
        directories = []
        if self.radioButtonWorkspace.isChecked():
            for project in self.application.projectManager.getAllProjects():
                self.model.addGroup(project.nodeName(), project.directory)
                directories.append(project.directory)
        self.fileSearchThread.searchInFiles(directories, filters, searchPattern, recursive, byPhrase)
        
    @classmethod
    def search(cls, model, parent = None):
        dlg = cls(model, parent)
        dlg.exec_()
