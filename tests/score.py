
import os, sys
sys.path.append(os.path.abspath('..'))

def test_score(sp):
    reference_scope = 'text.html.basic source.php.embedded.html string.quoted.double.php'
      
    sp.score( 'source.php string', reference_scope )
    sp.score( 'text.html source.php', reference_scope )
    sp.score( 'string source.php', reference_scope )
    sp.score( 'source.php text.html', reference_scope )
      
    sp.score( 'text.html source.php - string', reference_scope )
    sp.score( 'text.html source.php - ruby', reference_scope )
      
    sp.score( '', reference_scope )
    sp.score( 'source.php', reference_scope )
    sp.score( 'string', reference_scope )
    sp.score( 'source.php', reference_scope ) 
    sp.score( 'text source string', reference_scope )
    sp.score( 'source string', reference_scope )
      
    sp.score( 'text.html source.php - string', reference_scope )

if __name__ == "__main__":
    from time import time
    from prymatex.support.score import PMXScoreManager
    sp = PMXScoreManager()
    start = time()
    for _ in range(1000):
        test_score(sp)
    print "Time:", time() - start