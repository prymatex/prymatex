from bisect import bisect
from PyQt4 import QtCore, QtGui
from prymatex.support import PMXSyntax

class PMXEditorFolding(object):
    def __init__(self, editor):
        self.editor = editor
        self.indentSensitive = False
        self.editor.textChanged.connect(self.on_editor_textChanged)
        self.blocks = []
        self.folding = []

    def _purge_blocks(self, startIndex = None, endIndex = None):
        remove = filter(lambda block: block.userData() is None, self.blocks[startIndex:endIndex])
        if remove:
            startIndex = self.blocks.index(remove[0])
            endIndex = self.blocks.index(remove[-1])
            self.blocks = self.blocks[:startIndex] + self.blocks[endIndex + 1:]

    def on_editor_textChanged(self):
        #TODO: solo hacer las acciones si tengo nuevo estado de folding motivado por un remove o un add
        if not self.editor.isAutomatedAction():
            self._purge_blocks()
            self.updateFolding()

    def addFoldingBlock(self, block):
        if block not in self.blocks:
            indexes = map(lambda block: block.blockNumber(), self.blocks)
            index = bisect(indexes, block.blockNumber())
            self.blocks.insert(index, block)

    def removeFoldingBlock(self, block):
        index = self.blocks.index(block)
        #self._purge_blocks(startIndex = index)
        self.blocks.remove(block)

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
            if lastBlock in self.folding: return
            lessIndentBlock = self.editor.findPreviousLessIndentBlock(lastBlock)
            if lessIndentBlock is not None:
                nest += self.tryCloseIndentBlock(lessIndentBlock)
            else:
                nest += self.tryCloseIndentBlock(lastBlock)

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