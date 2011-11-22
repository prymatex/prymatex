from bisect import bisect
from PyQt4 import QtCore, QtGui
from prymatex.support import PMXSyntax

class PMXEditorFolding(object):
    def __init__(self, editor):
        self.editor = editor
        self.indentSensitive = False
        self.editor.blocksRemoved.connect(self.on_textBlocksRemoved)
        self.blocks = []
        self.folding = []

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
        self.updateFolding()
        
    def removeFoldingBlock(self, block):
        index = self.blocks.index(block)
        self._purge_blocks(startIndex = index)
        self.blocks.remove(block)
        self.updateFolding()

    def on_textBlocksRemoved(self, block, length):
        self._purge_blocks()
        self.updateFolding()
    
    def updateFolding(self):
        self.folding = []
        if self.indentSensitive:
            pass
            #self.updateIndentFoldingBlocks()
        else:
            self.updateFoldingBlocks()
        self.editor.sidebar.update()
        
    def updateFoldingBlocks(self):
        nest = 0
        for block in self.blocks:
            userData = block.userData()
            if userData is None: break #FIXME: PARCHAZO PARA VER
            nest += userData.foldingMark
            if nest >= 0:
                self.folding.append(block)

    def updateIndentFoldingBlocks(self):
        nest = 0
        lastOpenIndent = currentIndent = ""
        for block in self.blocks:
            userData = block.userData()
            if userData.foldingMark <= PMXSyntax.FOLDING_STOP:
                #Esta cerrando, si no puede cerrar nada continuo?
                if nest <= 0:
                    continue
            elif userData.foldingMark >= PMXSyntax.FOLDING_START:
                #Esta abriendo, esta menos indentado?
                if userData.indent <= currentIndent and len(self.folding) > 0:
                    #Hay que cerrar algo antes
                    closeBlock = self.editor.findPreviousMoreIndentBlock(block)
                    if closeBlock is not None:
                        lenIndent = len(userData.indent)
                        closeBlock.userData().foldingMark = - (len(currentIndent) / lenIndent) if lenIndent else -nest
                        self.folding.append(closeBlock)
                        nest += closeBlock.userData().foldingMark
                else:
                    #Store last valid indent
                    lastOpenIndent = currentIndent
            nest += userData.foldingMark
            currentIndent = userData.indent if userData.foldingMark >= PMXSyntax.FOLDING_START else lastOpenIndent
            if nest >= 0:
                self.folding.append(block)
        if nest > 0:
            #Quedo abierto, tengo que buscar el que cierra o uso el ultimo
            lastBlock = self.editor.document().lastBlock()
            openBlock = self.editor.findPreviousLessIndentBlock(lastBlock)
            if openBlock is None: return
            closeBlock = self.editor.findPreviousMoreIndentBlock(openBlock)
            if closeBlock is None: return
            lenIndent = len(closeBlock.userData().indent)
            closeBlock.userData().foldingMark = - (len(currentIndent) / lenIndent) if lenIndent else -nest
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