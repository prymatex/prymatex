from time import time

class TestScopes1(object):
    def __init__(self):
        self.scopes = []
        
    def addScope(self, begin, end, scope):
        for pos in xrange(end - begin):
            self.scopes.insert(begin + pos, scope)

class TestScopes2(object):
    def __init__(self):
        self.scopes = []
        
    def addScope(self, begin, end, scope):
        self.scopes[begin:end] = [scope for _ in xrange(end - begin)]
if __name__ == "__main__":
    scopes1 = TestScopes1()
    scopes2 = TestScopes2()
    now = time()
    for x in xrange(1000):
        scopes1.addScope(0, 80, "1")
        scopes1.addScope(30, 60, "2")
    print time() - now
    now = time()
    for x in xrange(1000):
        scopes2.addScope(0, 80, "1")
        scopes2.addScope(30, 60, "2")
    print time() - now
    print scopes1.scopes
    print scopes2.scopes
    print scopes1.scopes == scopes2.scopes