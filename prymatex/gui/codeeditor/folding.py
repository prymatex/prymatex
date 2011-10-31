from bisect import bisect
from PyQt4 import QtCore, QtGui
from prymatex.support import PMXSyntax

class PMXEditorFolding(object):
    def __init__(self, editor):
        self.editor = editor
        self.indentSensitive = False
        self.editor.foldingChanged.connect(self.on_foldingChanged)
        self.editor.textBlocksRemoved.connect(self.on_textBlocksRemoved)
        self.blocks = []
        self.folding = []

    def on_foldingChanged(self, block):
        if block in self.blocks:
            userData = block.userData()
            if userData.foldingMark == PMXSyntax.FOLDING_NONE:
                self.blocks.remove(block)
        else:
            indexes = map(lambda block: block.blockNumber(), self.blocks)
            index = bisect(indexes, block.blockNumber())
            self.blocks.insert(index, block)
        if self.indentSensitive:
            self.updateIndentFoldingBlocks()
        else:
            self.updateFoldingBlocks()
    
    def on_textBlocksRemoved(self):
        remove = filter(lambda block: block.userData() is None, self.blocks)
        if remove:
            sIndex = self.blocks.index(remove[0])
            eIndex = self.blocks.index(remove[-1])
            self.blocks = self.blocks[:sIndex] + self.blocks[eIndex + 1:]
        if self.indentSensitive:
            self.updateIndentFoldingBlocks()
        else:
            self.updateFoldingBlocks()
        
    def updateFoldingBlocks(self):
        self.folding = []
        nest = 0
        for block in self.blocks:
            userData = block.userData()
            nest += userData.foldingMark
            if nest >= 0:
                self.folding.append(block)

    def updateIndentFoldingBlocks(self):
        self.folding = []
        nest = 0
        lastOpenIndent = currentIndent = ""
        for block in self.blocks:
            userData = block.userData()
            if userData.foldingMark <= PMXSyntax.FOLDING_STOP:
                #Esta cerrando, es blank?
                if block.text().strip() == "":
                    continue
            elif userData.foldingMark >= PMXSyntax.FOLDING_START:
                #Esta abriendo, esta menos indentado?
                if userData.indent <= currentIndent and len(self.folding) > 0:
                    #Hay que cerrar algo antes
                    closeBlock = self.findPreviousMoreIndentBlock(block)
                    lenIndent = len(userData.indent)
                    if lenIndent:
                        closeBlock.userData().foldingMark = - (len(currentIndent) / lenIndent)
                    else:
                        closeBlock.userData().foldingMark = -nest
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
            #Tengo que cerrar el ultimo
            closeBlock = self.editor.document().lastBlock()
            userData = closeBlock.userData()
            if userData is not None:
                closeBlock.userData().foldingMark = -nest
                self.folding.append(closeBlock)

    def findPreviousMoreIndentBlock(self, block):
        """ Return previous block if text in block is not bank """
        indent = block.userData().indent
        while block.isValid():
            block = block.previous()
            if indent < block.userData().indent:
                break
        return block
    
    def getFoldingMark(self, block):
        if block in self.folding:
            userData = block.userData()
            return userData.foldingMark
        return PMXSyntax.FOLDING_NONE
    
    def findBlockFoldClose(self, block):
        nest = 0
        assert block in self.folding, "The block is not in folding"
        index = self.folding.index(block)
        for block in self.folding[index:]:
            userData = block.userData()
            if userData.foldingMark >= PMXSyntax.FOLDING_START or userData.foldingMark <= PMXSyntax.FOLDING_STOP:
                nest += userData.foldingMark
            if nest <= 0:
                break
        #return the founded block or the last valid block
        return block if block.isValid() else block.previous()
    
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
                break

        #return the founded block or the first valid block
        return block if block.isValid() else block.next()
    
    def getNestedLevel(self, index):
        return reduce(lambda x, y: x + y, map(lambda block: block.userData().foldingMark, self.folding[:index]), 0)
        
    def isStart(self, mark):
        return mark >= PMXSyntax.FOLDING_START

    def isStop(self, mark):
        return mark <= PMXSyntax.FOLDING_STOP
        
    def isFoldingMark(self, block):
        return block in self.folding