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
    now = time()
    r1 = []
    r2 = []
    for x in xrange(10000):
        scopes1 = TestScopes1()
        scopes1.addScope(0, 80, "1")
        scopes1.addScope(30, 60, "2")
        scopes1.addScope(10, 20, "3")
        scopes1.addScope(64, 70, "4")
        scopes1.addScope(24, 100, "5")
        r1 = scopes1.scopes
    print time() - now
    now = time()
    for x in xrange(10000):
        scopes2 = TestScopes2()
        scopes2.addScope(0, 80, "1")
        scopes2.addScope(30, 60, "2")
        scopes2.addScope(10, 20, "3")
        scopes2.addScope(64, 70, "4")
        scopes2.addScope(24, 100, "5")
        r2 = scopes2.scopes
    print time() - now
    print len(r1)
    print len(r2)
    print r1 == r2
    