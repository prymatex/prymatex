#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bisect import bisect
from PyQt4 import QtCore, QtGui
from prymatex.support import PMXSyntax

class PMXEditorFolding(object):
    def __init__(self, editor):
        self.editor = editor
        self.logger = editor.application.getLogger('.'.join([self.__class__.__module__, self.__class__.__name__]))
        self.indentSensitive = False
        self.foldingUpdated = True
        self.editor.textChanged.connect(self.on_editor_textChanged)
        self.blocks = []
        self.folding = []

    def _purge_blocks(self):
        def validFoldingBlock(block):
            return block.userData() is not None and block.userData().foldingMark != None
        self.blocks = filter(validFoldingBlock, self.blocks)

    def on_editor_textChanged(self):
        if not self.foldingUpdated:
            self.logger.debug("Purgar y actualizar folding")
            self._purge_blocks()
            self.updateFolding()
            self.foldingUpdated = True

    def addFoldingBlock(self, block):
        if block not in self.blocks:
            indexes = map(lambda block: block.blockNumber(), self.blocks)
            index = bisect(indexes, block.blockNumber())
            self.blocks.insert(index, block)
            self.foldingUpdated = False
        
    def removeFoldingBlock(self, block):
        if block in self.blocks:
            index = self.blocks.index(block)
            self.blocks.remove(block)
            self.foldingUpdated = False
        
    def updateFolding(self):
        self.folding = []
        if self.indentSensitive:
            self.updateIndentFoldingBlocks()
        else:
            self.updateFoldingBlocks()
        self.editor.sidebar.update()

    def updateFoldingBlocks(self):
        nest = 0
        for block in self.blocks:
            userData = block.userData()
            nest += userData.foldingMark
            if nest >= 0:
                self.folding.append(block)

    def findPreviousEqualIndentOpenBlock(self, block):
        block = self.editor.findPreviousEqualIndentBlock(block)
        while block is not None and not self.isStart(block.userData().foldingMark):
            block = self.editor.findPreviousEqualIndentBlock(block)
        if block is not None:
            return block
    
    def tryCloseIndentBlock(self, block):
        #Buscar si corresponde cerrar algo antes
        openBlock = self.findPreviousEqualIndentOpenBlock(block)
        if openBlock is not None:
            #Hay que cerrar algo antes
            realBlock = self.editor.findPreviousEqualIndentBlock(block)
            while realBlock != openBlock:
                block = realBlock
                realBlock = self.editor.findPreviousEqualIndentBlock(realBlock)
            closeBlock = self.editor.findPreviousMoreIndentBlock(block)
            if closeBlock is not None:
                closeBlock.userData().foldingMark = self.getNestedLevel(openBlock) - self.getNestedLevel(closeBlock)
                self.folding.append(closeBlock)
                return closeBlock.userData().foldingMark
        return 0
    
    def updateIndentFoldingBlocks(self):
        nest = 0
        for block in self.blocks:
            userData = block.userData()
            if self.isStop(userData.foldingMark) and block.text().strip() == "":
                continue
            elif self.isStart(userData.foldingMark):
                nest += self.tryCloseIndentBlock(block)
            nest += userData.foldingMark
            if nest >= 0:
                self.folding.append(block)
        if nest > 0:
            #TODO: Arreglar esto que no depende de block
            lastBlock = self.editor.document().lastBlock()
            if lastBlock.text().strip() == "":
                lastBlock = self.editor.findPreviousNoBlankBlock(lastBlock)
            if lastBlock in self.folding: return
            lessIndentBlock = self.editor.findPreviousLessIndentBlock(lastBlock)
            if lessIndentBlock is not None:
                nest += self.tryCloseIndentBlock(lessIndentBlock)
            else:
                nest += self.tryCloseIndentBlock(lastBlock)
            if nest > 0:
                lastBlock.userData().foldingMark = -nest
                self.folding.append(lastBlock)

    def getFoldingMark(self, block):
        if block in self.folding:
            userData = block.userData()
            return userData.foldingMark
    
    def findBlockFoldClose(self, block):
        nest = 0
        assert block in self.folding, "The block is not in folding"
        index = self.folding.index(block)
        for block in self.folding[index:]:
            userData = block.userData()
            if userData.foldingMark >= PMXSyntax.FOLDING_START or userData.foldingMark <= PMXSyntax.FOLDING_STOP:
                nest += userData.foldingMark
            if nest <= 0:
                return block
    
    def findBlockFoldOpen(self, block):
        nest = 0
        assert block in self.folding, "The block is not in folding"
        index = self.folding.index(block)
        folding = self.folding[:index + 1]
        folding.reverse()
        for block in folding:
            userData = block.userData()
            if userData.foldingMark >= PMXSyntax.FOLDING_START or userData.foldingMark <= PMXSyntax.FOLDING_STOP:
                nest += userData.foldingMark
            if nest >= 0:
                return block
    
    def getNestedLevel(self, block):
        blocks = filter(lambda fblock: fblock.blockNumber() < block.blockNumber(), self.folding)
        return reduce(lambda x, y: x + y, map(lambda block: block.userData().foldingMark, blocks), 0)
        
    def isStart(self, mark):
        if mark is None: return False
        return mark >= PMXSyntax.FOLDING_START

    def isStop(self, mark):
        if mark is None: return False
        return mark <= PMXSyntax.FOLDING_STOP

    def isFolded(self, block):
        return self.isFoldingMark(block) and block.userData().folded
    
    def isFoldingMark(self, block):
        return block in self.folding