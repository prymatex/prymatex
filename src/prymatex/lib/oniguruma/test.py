import unittest


class OnigRegex(unittest.TestCase):
    
    
        
    
    def setUp(self):
        import pyonig #@UnresolvedImport @UnusedImport
        self.wrapping_module = pyonig #@UndefinedVariable
        self.assertTrue(hasattr(self.wrapping_module, 'Regex'))
        
    
    def test_match(self):
        ''''''
        regex = self.wrapping_module.Regex('a')
        match = regex.match('abababa')
        self.assertNotEqual(match, None)
        
    def test_not_match(self):
        '''
        '''
        regex = self.wrapping_module.Regex('aab')
        match = regex.match('az')
        self.assertEqual(match, None)
    
    def test_names(self):
        pass
        
if __name__ == "__main__":
    unittest.main()