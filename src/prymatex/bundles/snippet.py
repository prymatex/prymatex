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
              {'match': '\\$(\\d+)',
               'captures': {'1': {'name': 'keyword.tabstop.snippet'}},
               'name': 'meta.referred.tabstop.snippet'},
              {'begin': '\\$\\{(\\d+):',
               'beginCaptures': {'1': {'name': 'keyword.tabstop.snippet'}},
               'contentName': 'string.default',
               'end': '\\}',
               'name': 'meta.structure.tabstop.snippet',
               'patterns': [{'include': '$self'}]},
              {'begin': '\\$\\{(\\d+)/',
               'beginCaptures': {'1': {'name': 'keyword.tabstop.snippet'}},
               'contentName': 'string.regexp',
               'end': '\\}',
               'name': 'meta.structure.tabstop.snippet',
               'patterns': [{'include': '#escaped_char'},
                            {'include': '#substitution'}]},
              {'captures': {'1': {'name': 'string.env.snippet'}},
               'match': '\\$([a-zA-Z_][a-zA-Z0-9_]*)',
               'name': 'meta.structure.variable.snippet'},
              {'begin': '\\$\\{([a-zA-Z_][a-zA-Z0-9_]*):',
               'beginCaptures': {'1': {'name': 'string.env.snippet'}},
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
                                 'beginCaptures': {'0': {'name': 'entity.name.function.snippet'}},
                                 'contentName': 'text.substitution',
                                 'end': '/[mg]?',
                                 'endCaptures': {'0': {'name': 'entity.name.function.snippet'}},
                                 'patterns': [{'include': '#escaped_char'},
                                              {'include': '#replacements'},
                                              {'include': '#condition'}]}}
 }

#Snippet nodes
class Node(object):
    def __init__(self, name):
        self.name = name
        
    def render(self, context):
        "Return the node rendered as a string"
        pass
    
class NodeList(list):
    def __init__(self, name):
        super(NodeList, self).__init__()
        self.name = name

    def append(self, element):
        element.parent = self
        super(NodeList, self).append(element)
        return element

class TextNode(Node):
    def __init__(self, name, text):
        super(TextNode, self).__init__(name)
        self.text = text

    def __repr__(self):
        return "<%s Node: '%s'>" % (self.name, self.text)
        
    def render(self, context):
        return self.text

class RegexpNode(Node):
    def __init__(self, name):
        self.regexp = None
        self.format = None
        self.options = None

class TabstopNode(NodeList):
    def __init__(self, name):
        super(TabstopNode, self).__init__(name)
        self.index = 0
        
    def __repr__(self):
        return "<TabstopNode %d: '%s'>" % (self.index, super(NodeList, self).__repr__())

class ShellNode(NodeList):
    pass
    
class PMXSnippetProcessor(PMXSyntaxProcessor):
    def __init__(self, snippet, text):
        self.snippet = snippet
        self.text = text
        self.line = 0
        self.node = NodeList("snippet")

    def open_tag(self, name, start):
        if name == 'meta.structure.tabstop.snippet':
            self.node.append(TextNode("string", self.current[self.index:start]))
            self.node = self.node.append(TabstopNode(name))
        elif name == 'string.regexp':
            self.node = self.node.append(RegexpNode(name, self.current[self.index:end]))
        elif name == 'string.interpolated.shell.snippet':
            self.node = self.node.append(ShellNode(name))
        self.index = start
        
    def close_tag(self, name, end):
        if name == 'meta.structure.tabstop.snippet':
            self.node = self.node.parent
        elif name == 'keyword.tabstop.snippet':
            self.node.index = int(self.current[self.index:end])
        elif name == 'string.default':
            self.node.append(TextNode(name, self.current[self.index:end]))
        elif name == 'string.regexp':
            self.node = self.node.append(RegexpNode(name, self.current[self.index:end]))
        elif name == 'string.interpolated.shell.snippet':
            self.node.append(TextNode(name, self.current[self.index:end]))
            self.node = self.node.parent
        self.index = end

    def new_line(self, line):
        self.current = self.text[self.line]
        self.line += 1
        self.index = 0
        if getattr(self.node, 'name') != "snippet":
            self.node.append(TextNode(self.node.name, self.current[self.index:]))

    def start_parsing(self, name):
        print "start", self.node

    def end_parsing(self, name):
        print "end", self.node

class PMXSnippet(PMXBundleItem):
    parser = PMXSyntax(SNIPPET_SYNTAX)
    def __init__(self, hash, name_space = "default"):
        super(PMXSnippet, self).__init__(hash, name_space)
        for key in [    'content', 'disableAutoIndent', 'inputPattern', 'bundlePath' ]:
            setattr(self, key, hash.pop(key, None))
    
    def compile(self):
        text = self.content.splitlines()
        processor = PMXDebugSyntaxProcessor()
        #processor = PMXSnippetProcessor(self, text)
        self.parser.parse(self.content, processor)
  