'''
Blacklisting paths
'''

import re
import sys
class blacklister(object):
    def __init__(self, blacklist = None, whitelist = None):
        if not blacklist and not whitelist:
            self.bypass = True
        else:
            self.bypass = False
            self.blacklist = self._make_list(blacklist)
            self.whitelist = self._make_list(whitelist)
        

    def __call__(self, path):
        return self.test(path)

    def test(self, path):
        if self.bypass:
            return True # All return OK if the filter is bypassed
        if self.backlist:
            if self.blacklist.has( path ):
                if self.whitelist.has ( path ):
                    return True # Whitelisted
                return False # Is in blacklist and not whitelited explicitly
            return True #
        elif self.whitelist:
            if self.whitelist.has( path ):
                return True
            return False
                
            
def test():
    f
    tester = blacklister()
    for elem in ['a', 'b', 'c']:
        print tester(elem)
    tester2 = tester('*', 'Python.tmbundle')
    python_and_others = ['/usr/bin/Python.tmbundle', '../Bash.tmbundle',
                         '']
    for pth in python_and_others:
        

if __name__ == "__main__":
    sys.exit(test())
