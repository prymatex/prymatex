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

import ponyguruma as onig
from ponyguruma.constants import OPTION_CAPTURE_GROUP
import ipdb

onig_compile = onig.Regexp.factory(flags = OPTION_CAPTURE_GROUP)

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
 'repository': {'condition': {'begin': '\\(\\?(\\d):',
                              'beginCaptures': {'1': {'name': 'string.regexp.condition'}},
                              'contentName': 'text.condition',
                              'end': '\\)',
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
    def __init__(self, parent = None):
        self.parent = parent
        self.children = []
    
    def append(self, element):
        self.children.append(element)
    
    def clear(self):
        self.children = []
        
    def __iter__(self):
        return iter(self.children)
    
    def __str__(self):
        string = ""
        for child in self:
            string += str(child)
        return string
    
    def __contain__(self, element):
        if isinstance(element, str):
            return false
        else:
            return element in self.children
    
    def open(self, name, text):
        self.append(text)
        node = self
        if name == 'meta.structure.tabstop.snippet':
            node = Tabstop(self)
            self.append(node)
        elif name == 'meta.structure.placeholder.snippet':
            node = Placeholder(self)
            self.append(node)
        elif name == 'meta.structure.variable.snippet':
            node = Variable(self)
            self.append(node)
        elif name == 'meta.structure.transformation.snippet':
            node = Transformation(self)
            self.append(node)
        if node == None:
            print "no puedo con %s" % name
        return node
        
    def close(self, name, text):
        self.append(text)
        return self

    def get_nodes_by_type(self, nodetype):
        "Return a list of all nodes (within this node and its nodelist) of the given type"
        nodes = []
        if isinstance(self, nodetype):
            nodes.append(self)
        for node in self:
            if (hasattr(node, 'get_nodes_by_type')):
                nodes.extend(node.get_nodes_by_type(nodetype))
        return nodes

class Tabstop(Node):
    def __init__(self, parent = None):
        super(Tabstop, self).__init__(parent)
        self.placeholder = None
        
    def __str__(self):
        if self.placeholder != None:
            return str(self.placeholder)
        else:
            return ""
        
    def open(self, name, text):
        node = self
        return node
        
    def close(self, name, text):
        if name == 'meta.structure.tabstop.snippet':
            return self.parent
        elif name == 'keyword.tabstop.snippet':
            self.index = int(text)
        return self

    def taborder(self, container):
        if type(container) == list:
            container.append(self)
        else:
            self.placeholder = container
        return container

class Placeholder(Node):
    def __init__(self, parent = None):
        super(Placeholder, self).__init__(parent)
        self.mirrors = []

    def open(self, name, text):
        node = self
        if name == 'meta.structure.tabstop.snippet':
            self.append(text)
            node = Tabstop(self)
            self.append(node)
        elif name == 'meta.structure.placeholder.snippet':
            self.append(text)
            node = Placeholder(self)
            self.append(node)
        elif name == 'string.interpolated.shell.snippet':
            node = Shell(self)
            self.append(node)
        return node

    def close(self, name, text):
        if name == 'meta.structure.placeholder.snippet':
            return self.parent
        elif name == 'keyword.placeholder.snippet':
            self.index = int(text)
        elif name == 'string.default':
            self.append(text)
        return self

    def taborder(self, container):
        if type(container) == list and container:
            for element in container:
                element.placeholder = self
        return self

    def write(self, text):
        self.clear()
        self.append(text)
            
class Transformation(Node):
    def __init__(self, parent = None):
        super(Transformation, self).__init__(parent)
        self.placeholder = None
    
    def __str__(self):
        text = ""
        if self.placeholder != None:
            text = str(self.placeholder)
        return self.children[0].transform(text)
    
    def open(self, name, text):
        node = self
        if name == 'string.regexp':
            node = Regexp(self)
            self.append(node)
        return node
        
    def close(self, name, text):
        if name == 'meta.structure.transformation.snippet':
            return self.parent
        elif name == 'keyword.transformation.snippet':
            self.index = int(text)
        return self
    
    def taborder(self, container):
        if type(container) == list:
            container.append(self)
        else:
            self.placeholder = container
        return container
        
class Variable(Node):
    def open(self, name, text):
        node = self
        if name == 'string.regexp':
            node = Regexp(self)
            self.append(node)
        return node
        
    def close(self, name, text):
        if name == 'meta.structure.variable.snippet':
            return self.parent
        elif name == 'string.env.snippet':
            self.string = text
        elif name == 'string.default':
            self.append(text)
        return self

class Regexp(Node):
    def __init__(self, parent = None):
        super(Regexp, self).__init__(parent)
        self.pattern = ""
        self.options = ""

    def open(self, name, text):
        node = self
        #FIXME: Correct syntax
        if name == 'text.substitution':
            self.pattern = onig_compile(text[:-1])
            node = Substitution(self)
            self.append(node)
        return node

    def close(self, name, text):
        if name == 'string.regexp':
            return self.parent
        elif name == 'string.regexp.options':
            self.options = text
        return self
    
    def sub(self, match):
        return self.children[0].sub(match)
            
    def transform(self, text):
        return self.pattern.sub(lambda match: self.sub(match), text)

class Substitution(Node):
    def open(self, name, text):
        node = self
        if name == 'meta.structure.condition.regexp':
            node = Condition(self)
            self.append(node)
        return node
    
    def close(self, name, text):
        if name == 'text.substitution':
            self.append(text)
            return self.parent
        return self
        
    def sub(self, match):
        if isinstance(self.children[0], Condition):
            print dir(match[2])
            return str(self.children[0]) + match[self.children[0].index]
        else:
            return str(self)

class Condition(Node):
    def open(self, name, text):
        node = self
        print "open", name, text
        return node
    
    def close(self, name, text):
        print "close", name, text
        if name == 'meta.structure.condition.regexp':
            return self.parent
        elif name == 'string.regexp.condition':
            self.index = int(text)
        elif name == 'text.condition':
            self.append(text)
        return self
        
class Shell(Node):
    def open(self, name, text):
        node = self
        return node
        
    def close(self, name, text):
        self.append(text)
        if name == 'string.interpolated.shell.snippet':
            return self.parent
        return self
        
class PMXSnippetProcessor(PMXSyntaxProcessor):
    def __init__(self):
        self.current = None
        self.node = Node("root")
        self.taborder = {}

    def open_tag(self, name, start):
        token = self.current[self.index:start]
        self.node = self.node.open(name, token)
        self.index = start
        
    def close_tag(self, name, end):
        token = self.current[self.index:end]
        self.node = self.node.close(name, token)
        if hasattr(self.node, 'index') and callable(getattr(self.node, 'taborder', None)):
            container = self.taborder.setdefault(self.node.index, [])
            if (self.node != container and self.node not in container):
                self.taborder[self.node.index] = self.node.taborder(container)
        self.index = end

    def new_line(self, line):
        if self.current != None and self.index != len(self.current):
            self.node.append(self.current[self.index:len(self.current)] + "\n")
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
        self.taborder = processor.taborder
    
    def write(self, taborder, text):
        self.taborder[taborder].write(text)

    def __str__(self):
        return str(self.node)