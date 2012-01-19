from bisect import bisect
from PyQt4 import QtCore, QtGui
from prymatex.support import PMXSyntax

class PMXEditorFolding(object):
    def __init__(self, editor):
        self.editor = editor
        self.indentSensitive = False
        self.editor.blocksRemoved.connect(self.on_editor_textBlocksRemoved)
        self.editor.foldingUpdateRequest.connect(self.on_editor_textBlocksRemoved)
        self.blocks = []
        self.folding = []

    def on_editor_textBlocksRemoved(self, block = None, length = None):
        self._purge_blocks()
        self.updateFolding()

    def _purge_blocks(self, startIndex = None, endIndex = None):
        remove = filter(lambda block: block.userData() is None, self.blocks[startIndex:endIndex])
        if remove:
            startIndex = self.blocks.index(remove[0])
            endIndex = self.blocks.index(remove[-1])
            self.blocks = self.blocks[:startIndex] + self.blocks[endIndex + 1:]

    def addFoldingBlock(self, block):
        if block not in self.blocks:
            indexes = map(lambda block: block.blockNumber(), self.blocks)
            index = bisect(indexes, block.blockNumber())
            self.blocks.insert(index, block)

    def removeFoldingBlock(self, block):
        try:
            index = self.blocks.index(block)
            self._purge_blocks(startIndex = index)
            self.blocks.remove(block)
        except ValueError:
            self._purge_blocks()

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

    def findPreviousEqualIndentOpenBlock(self, block, indent):
        block = self.editor.findPreviousEqualIndentBlock(block, indent)
        while block is not None and not self.isStart(block.userData().foldingMark):
            block = self.editor.findPreviousEqualIndentBlock(block, indent)
        if block is not None:
            return block
            
    def updateIndentFoldingBlocks(self):
        nest = 0
        for block in self.blocks:
            userData = block.userData()
            if self.isStop(userData.foldingMark) and userData.indentLength == -1:
                continue
            elif self.isStart(userData.foldingMark):
                #Buscar si corresponde cerrar algo antes
                openBlock = self.findPreviousEqualIndentOpenBlock(block, userData.indent)
                if openBlock is not None:
                    #Hay que cerrar algo antes
                    closeBlock = self.editor.findPreviousMoreIndentBlock(block)
                    if closeBlock is not None:
                        #TODO: Aca va un valor en funcion de que valor esta cerrando, cuidado con el -1 de error
                        indentDiff = openBlock.userData().indentLength - block.userData().indentLength
                        print openBlock.text()
                        print indentDiff, self.editor.tabStopSize, indentDiff / self.editor.tabStopSize, self.getNestedLevel(self.folding.index(openBlock))
                        closeBlock.userData().foldingMark = -(self.getNestedLevel(self.folding.index(openBlock)) - indentDiff / self.editor.tabStopSize)
                        self.folding.append(closeBlock)
                        nest += closeBlock.userData().foldingMark
            nest += userData.foldingMark
            if nest >= 0:
                self.folding.append(block)
        if nest != 0:
            print "quedo abierto"
            #Quedo abierto, tengo que buscar el que cierra o uso el ultimo
            lastBlock = self.editor.document().lastBlock()
            if lastBlock in self.folding: return
            openBlock = self.editor.findPreviousLessIndentBlock(lastBlock)
            if openBlock is None:
                closeBlock = self.editor.findPreviousMoreIndentBlock(lastBlock)
                if closeBlock is not None:
                    closeBlock.userData().foldingMark = -nest
                    self.folding.append(closeBlock)
            else:
                closeBlock = self.editor.findPreviousMoreIndentBlock(openBlock)
                if closeBlock is not None:
                    closeBlock.userData().foldingMark = -nest
                    self.folding.append(closeBlock)
            
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
    
    def getNestedLevel(self, index):
        return reduce(lambda x, y: x + y, map(lambda block: block.userData().foldingMark, self.folding[:index]), 0)
        
    def isStart(self, mark):
        if mark is None: return False
        return mark >= PMXSyntax.FOLDING_START

    def isStop(self, mark):
        if mark is None: return False
        return mark <= PMXSyntax.FOLDING_STOP

    def isFoldingMark(self, block):
        return block in self.folding