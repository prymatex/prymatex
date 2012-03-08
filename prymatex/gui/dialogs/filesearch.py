#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Based on Ninja IDE https://github.com/ninja-ide/ninja-ide/blob/master/ninja_ide/gui/misc/find_in_files.py
import os
import Queue

from PyQt4 import QtCore, QtGui

from prymatex.ui.dialogs.search import Ui_SearchDialog
from prymatex.models.tree import TreeNode, TreeModel

class FileSearchThread(QtCore.QThread):
    foundPattern = QtCore.pyqtSignal(str, list)
    
    def searchInFiles(self, directories, filePattern, searchPattern, recursive, by_phrase):
        self._cancel = False
        self.recursive = recursive
        self.searchPattern = searchPattern
        self.filePatterns = filePattern.split(";")
        self.by_phrase = by_phrase
        self.queue = Queue.Queue()
        for directory in directories:
            self.queue.put(directory)
        #Start!
        self.start()

    def run(self):
        file_filter = QtCore.QDir.Files | QtCore.QDir.NoDotAndDotDot | QtCore.QDir.Readable
        dir_filter = QtCore.QDir.Dirs | QtCore.QDir.NoDotAndDotDot | QtCore.QDir.Readable
        while not self._cancel and not self.queue.empty():
            current_dir = QtCore.QDir(self.queue.get())
            #Skip not readable dirs!
            if not current_dir.isReadable():
                continue

            #Collect all sub dirs!
            if self.recursive:
                current_sub_dirs = current_dir.entryInfoList(dir_filter)
                for one_dir in current_sub_dirs:
                    self.queue.put(one_dir.absoluteFilePath())
            
            #QDir.entryInfoList (self, QStringList nameFilters, Filters filters = QDir.NoFilter, SortFlags sort = QDir.NoSort)
            current_files = current_dir.entryInfoList(self.filePatterns, file_filter)
            
            #process all files in current dir!
            for one_file in current_files:
                self._grep_file(one_file.absoluteFilePath(), one_file.fileName())

    def _grep_file(self, file_path, file_name):
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
        line_index = 0
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

class PMXFileSearchDialog(QtGui.QDialog, Ui_SearchDialog):
    def __init__(self, model, parent = None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.application = QtGui.QApplication.instance()
        self.model = model
        self.fileSearchThread = FileSearchThread()
        self.fileSearchThread.foundPattern.connect(self.on_fileSearchThread_foundPattern)
        
    def on_fileSearchThread_foundPattern(self, filePath, lines):
        if lines:
            self.model.addFileFound(filePath, lines)
        
    def on_buttonCancel_pressed(self):
        #FIXME: solo si esta corriendo
        print "cancelar"
        self.fileSearchThread.cancel()
        
    def on_buttonSearch_pressed(self):
        searchPattern = self.comboBoxContainingText.lineEdit().text()
        filters = self.comboBoxFilePatterns.lineEdit().text()
        recursive = True
        byPhrase = True
        #self.comboBoxWorkingSet
        #self.searchInFiles
        directories = []
        if self.radioButtonWorkspace.isChecked():
            for project in self.application.projectManager.getAllProjects():
                self.model.addGroup(project.name, project.directory)
                directories.append(project.directory)
        self.fileSearchThread.searchInFiles(directories, filters, searchPattern, recursive, byPhrase)
        
    @classmethod
    def search(cls, model, parent = None):
        dlg = cls(model, parent)
        dlg.exec_()
