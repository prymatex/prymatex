#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Based on Ninja IDE https://github.com/ninja-ide/ninja-ide/blob/master/ninja_ide/gui/misc/find_in_files.py
import Queue

from PyQt4 import QtCore, QtGui
from prymatex.ui.dialogs.search import Ui_Dialog

class FileFindThread(QtCore.QThread):
    foundPattern = QtCore.pyqtSignal(str, int)
    
    def findInFiles(self, dir_name, filters, reg_exp, recursive, by_phrase):
        self._cancel = False
        self.recursive = recursive
        self.search_pattern = reg_exp
        self.by_phrase = by_phrase
        self.filters = filters
        self.queue = Queue.Queue()
        self.queue.put(dir_name)
        self.root_dir = dir_name
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

            #all files in sub_dir first apply the filters
            current_files = current_dir.entryInfoList(
                self.filters, file_filter)
            #process all files in current dir!
            for one_file in current_files:
                self._grep_file(one_file.absoluteFilePath(),
                    one_file.fileName())

    def _grep_file(self, file_path, file_name):
        if not self.by_phrase:
            with open(file_path, 'r') as f:
                content = f.read()
            words = [word for word in \
                unicode(self.search_pattern.pattern()).split('|')]
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
            column = self.search_pattern.indexIn(line)
            if column != -1:
                lines.append((line_index, line))
            #take the next line!
            line = stream.readLine()
            if line.isNull():
                break
            line_index += 1
        #emit a signal!
        #relative_file_name = file_manager.convert_to_relative(self.root_dir, file_path)
        self.foundPattern.emit(file_path, lines)

    def cancel(self):
        self._cancel = True

class PMXFileFindDialog(QtGui.QDialog, Ui_Dialog):
    def __init__(self, parent = None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.fileFindThread = FileFindThread()
