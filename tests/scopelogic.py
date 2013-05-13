# coding: utf-8


test_string = "text.html -(meta.tag | source), invalid.illegal.incomplete.html -source"

class LogicRule(object):
    ''''''
    def __init__(self, rule_string):
        self._build_rule(rule_string)
        self._rule_string = rule_string
        
    def __eq__(self, other):
        return self._rule_string == other._rule_string
        
    def _build_rule(self, rule_string):
        assert isinstance(rule_string, str)
        sub_rules = rule_string.split(',')
        self.rule = None
        
    def match(self, scope):
        '''Check if socope matches with this rule'''
        pass
        

class PMXLogicDict(object):
    rules = {}
    
    def __init__(self,):
        """Un diccinario con la lógica de scopes"""
            
    def add_rule(self, name, obj):
        self.rules.append()
    
    def __getitem__(self, name):
        for logic, obj in self.__logic_mapping.items():
            if logic.match(name):
                return obj
                

def main():
    """Test"""
    logic = PMXLogicDict()
    logic.add_rule(test_string, 'test_string')
    logic.add_rule('source.python', 'python')
    logic.find('')


if __name__ == '__main__':
    main()