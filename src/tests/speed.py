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
        
class TestScopes3(object):
    def __init__(self):
        self.scopes = []
        
    def addScope(self, begin, end, scope):
        self.scopes = self.scopes[:begin] + [scope for _ in xrange(end - begin)] + self.scopes[end:]
        
if __name__ == "__main__":
    now = time()
    r1 = []
    r2 = []
    r3 = []
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
    now = time()
    for x in xrange(10000):
        scopes3 = TestScopes3()
        scopes3.addScope(0, 80, "1")
        scopes3.addScope(30, 60, "2")
        scopes3.addScope(10, 20, "3")
        scopes3.addScope(64, 70, "4")
        scopes3.addScope(24, 100, "5")
        r3 = scopes3.scopes
    print time() - now
    print len(r1)
    print len(r2)
    print len(r3)
    print r1 == r2
    