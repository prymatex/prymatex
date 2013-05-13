import os, sys
sys.path.append(os.path.abspath('..'))

from prymatex.gui.editor.codehelper import PMXFoldingHelper

def main(argv = sys.argv):
    folding = PMXFoldingHelper(None)
    folding.setStart(5)
    folding.setStop(8)
    folding.setStart(10)
    folding.setStart(15)
    folding.setStop(18)
    folding.setStop(20)
    print(folding.getNestedLevel(16))
    print(folding.start)
    print(folding.stop)
    return 0

if __name__ == "__main__":
    sys.exit(main())