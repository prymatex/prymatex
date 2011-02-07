#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    Snippte's module
'''
# for run as main
if __name__ == "__main__":
    import os, sys
    sys.path.append(os.path.abspath('../..'))
    
from prymatex.bundles.base import PMXBundleItem
from prymatex.bundles.processor import PMXSyntaxProcessor, PMXDebugSyntaxProcessor
from prymatex.bundles.syntax import PMXSyntax

SNIPPET_SYNTAX = {
 'patterns': [{'match': '\\\\(\\\\|\\$|`)',
               'name': 'constant.character.escape.snippet'},
              #TabStop
              {'captures': {'1': {'name': 'keyword.tabstop.snippet'}},
               'match': '\\$(\\d+)',
               'name': 'meta.structure.tabstop.snippet'},
              #Placeholder
              {'begin': '\\$\\{(\\d+):',
               'beginCaptures': {'1': {'name': 'keyword.placeholder.snippet'}},
               'contentName': 'string.default',
               'end': '\\}',
               'name': 'meta.structure.placeholder.snippet',
               'patterns': [{'include': '$self'}]},
              #Transformation
              {'begin': '\\$\\{(\\d+)/',
               'beginCaptures': {'1': {'name': 'keyword.transformation.snippet'}},
               'contentName': 'string.regexp',
               'end': '\\}',
               'name': 'meta.structure.transformation.snippet',
               'patterns': [{'include': '#escaped_char'},
                            {'include': '#substitution'}]},
              # Variables 
              {'match': '\\$([a-zA-Z_][a-zA-Z0-9_]*)',
               'captures': {'1': {'name': 'string.env.snippet'}},
               'name': 'meta.structure.variable.snippet'},
              {'begin': '\\$\\{([a-zA-Z_][a-zA-Z0-9_]*):',
               'beginCaptures': {'1': {'name': 'string.env.snippet'}},
               'contentName': 'string.default',
               'end': '\\}',
               'name': 'meta.structure.variable.snippet',
               'patterns': [{'include': '$self'}]},
              {'begin': '\\$\\{([a-zA-Z_][a-zA-Z0-9_]*)/',
               'beginCaptures': {'1': {'name': 'string.env.snippet'}},
               'contentName': 'string.regexp',
               'end': '\\}',
               'name': 'meta.structure.substitution.snippet',
               'patterns': [{'include': '#escaped_char'},
                            {'include': '#substitution'}]},
              {'begin': '`',
               'end': '`',
               'name': 'string.interpolated.shell.snippet'}],
 'repository': {'condition': {'begin': '\\(\\?\\d:',
                              'beginCaptures': {'0': {'name': 'string.regexp.condition'}},
                              'end': '\\)',
                              'endCaptures': {'0': {'name': 'string.regexp.condition'}},
                              'name': 'meta.structure.condition.regexp',
                              'patterns': [{'include': '#replacements'},
                                           {'begin': ':',
                                            'beginCaptures': {'0': {'name': 'string.regexp.condition'}},
                                            'end': '(?=\\))',
                                            'name': 'meta.structure.condition.regexp',
                                            'patterns': [{'include': '#replacements'}]}]},
                'escaped_char': {'match': '\\\\[/\\\\]',
                                 'name': 'constant.character.escape.regex'},
                'replacements': {'match': '\\$\\d|\\\\[uUILE]',
                                 'name': 'string.regexp.replacement'},
                'substitution': {'begin': '/',
                                 'contentName': 'text.substitution',
                                 'end': '/([mg]?)',
                                 'endCaptures': {'1': {'name': 'string.regexp.options'}},
                                 'patterns': [{'include': '#escaped_char'},
                                              {'include': '#replacements'},
                                              {'include': '#condition'}]}},
}

#Snippet nodes
class Node(object):
    def __init__(self, name, parent = None):
        self.name = name
        self.parent = parent
        self.children = []
    
    def __str__(self):
        string = ""
        for child in self.children:
            string += str(child)
        return string
        
    def open(self, name, text):
        self.children.append(text)
        node = self
        if name == 'meta.structure.tabstop.snippet':
            node = Tabstop(name, self)
            self.children.append(node)
        elif name == 'meta.structure.placeholder.snippet':
            node = Placeholder(name, self)
            self.children.append(node)
        elif name == 'meta.structure.variable.snippet':
            node = Variable(name, self)
            self.children.append(node)
        elif name == 'meta.structure.transformation.snippet':
            node = Transformation(name, self)
            self.children.append(node)
        if node == None:
            print "no puedo con %s" % name
        return node
        
    def close(self, name, text):
        self.children.append(text)
        return self

    def get_nodes_by_type(self, nodetype):
        "Return a list of all nodes (within this node and its nodelist) of the given type"
        nodes = []
        if isinstance(self, nodetype):
            nodes.append(self)
        for node in self.children:
            if (hasattr(node, 'get_nodes_by_type')):
                nodes.extend(node.get_nodes_by_type(nodetype))
        return nodes

class Tabstop(Node):
    def open(self, name, text):
        node = self
        return node
        
    def close(self, name, text):
        if name == 'meta.structure.tabstop.snippet':
            return self.parent
        elif name == 'keyword.tabstop.snippet':
            self.index = int(text)
        return self

class Placeholder(Node):
    def __init__(self, name, parent = None):
        super(Placeholder, self).__init__(name, parent)
        self.mirrors = []

    def open(self, name, text):
        node = self
        if name == 'meta.structure.tabstop.snippet':
            self.children.append(text)
            node = Tabstop(name, self)
            self.children.append(node)
        elif name == 'meta.structure.placeholder.snippet':
            self.children.append(text)
            node = Placeholder(name, self)
            self.children.append(node)
        elif name == 'string.regexp':
            node = Regexp(name, self)
            self.children.append(node)
        elif name == 'string.interpolated.shell.snippet':
            node = Shell(name, self)
            self.children.append(node)
        return node

    def close(self, name, text):
        if name == 'meta.structure.placeholder.snippet':
            return self.parent
        elif name == 'keyword.placeholder.snippet':
            self.index = int(text)
        elif name == 'string.default':
            self.children.append(text)
        return self

    def write(self, text):
        self.children = [text]
        for mirror in self.mirrors:
            mirror.write(text)
            
class Transformation(Node):
    def open(self, name, text):
        node = self
        if name == 'string.regexp':
            node = Regexp(name, self)
            self.children.append(node)
        return node
        
    def close(self, name, text):
        if name == 'meta.structure.transformation.snippet':
            return self.parent
        elif name == 'keyword.transformation.snippet':
            self.index = int(text)
        return self
        
class Variable(Node):
    def open(self, name, text):
        node = self
        if name == 'string.regexp':
            node = Regexp(name, self)
            self.children.append(node)
        return node
        
    def close(self, name, text):
        if name == 'meta.structure.variable.snippet':
            return self.parent
        elif name == 'string.env.snippet':
            self.string = text
        elif name == 'string.default':
            self.children.append(text)
        return self

class Regexp(Node):
    def __init__(self, name, parent = None):
        super(Regexp, self).__init__(name, parent)
        self.pattern = ""
        self.options = ""
        
    def open(self, name, text):
        node = self
        if name == 'text.substitution':
            self.pattern = text
        return node
        
    def close(self, name, text):
        if name == 'string.regexp':
            return self.parent
        elif name == 'text.substitution':
            self.children.append(text)
        elif name == 'string.regexp.options':
            self.options = text
        return self

class Shell(Node):
    def open(self, name, text):
        node = self
        return node
        
    def close(self, name, text):
        self.children.append(text)
        if name == 'string.interpolated.shell.snippet':
            return self.parent
        return self
        
class PMXSnippetProcessor(PMXSyntaxProcessor):
    def __init__(self):
        self.current = None
        self.node = Node("root")

    def open_tag(self, name, start):
        token = self.current[self.index:start]
        self.node = self.node.open(name, token)
        self.index = start
        
    def close_tag(self, name, end):
        token = self.current[self.index:end]
        self.node = self.node.close(name, token)
        self.index = end

    def new_line(self, line):
        if self.current != None and self.index != len(self.current):
            self.node.children.append(self.current[self.index:len(self.current)] + "\n")
        self.current = line
        self.index = 0
        
    def start_parsing(self, name):
        self.node.open(name, "")

    def end_parsing(self, name):
        token = self.current[self.index:len(self.current)]
        self.node.close(name, token)
        
class PMXSnippet(PMXBundleItem):
    parser = PMXSyntax(SNIPPET_SYNTAX)
    def __init__(self, hash, name_space = "default"):
        super(PMXSnippet, self).__init__(hash, name_space)
        for key in [    'content', 'disableAutoIndent', 'inputPattern', 'bundlePath' ]:
            setattr(self, key, hash.pop(key, None))
    
    def compile(self):
        text = self.content.splitlines()
        processor = PMXDebugSyntaxProcessor()
        processor = PMXSnippetProcessor()
        self.parser.parse(self.content, processor)
        self.node = processor.node
        self.resolve()
    
    def resolve(self):
        tabstops = map(lambda t: (t.index, t), self.node.get_nodes_by_type(Tabstop))
        taborder = placeholders = map(lambda p: (p.index, p), self.node.get_nodes_by_type(Placeholder))
        for po, placeholder in placeholders:
            for to, tabstop in tabstops:
                if po == to:
                    placeholder.mirrors.append(tabstop)
        others = set(map(lambda (o, t): o, tabstops)).difference(map(lambda (o, t): o, taborder))
        taborder.extend(filter(lambda (o, t): o in others, tabstops))
        self.taborder = map(lambda (order, node): node, sorted(taborder, key = lambda (order, _): order))

    def __str__(self):
        return str(self.node)