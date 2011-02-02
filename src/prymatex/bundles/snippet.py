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

SNIPPET_SYNTAX = {'name': 'Snippet',
'patterns': [{'match': '\\\\(\\\\|\\$|`)',
               'name': 'constant.character.escape.snippet'},
              {'captures': {'1': {'name': 'keyword.tabstop.snippet'}},
               'match': '\\$(\\d+)',
               'name': 'meta.structure.tabstop.snippet'},
              {'begin': '\\$\\{(\\d+):',
               'beginCaptures': {'1': {'name': 'keyword.tabstop.snippet'}},
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
                                              {'include': '#condition'}]}},
 'scopeName': 'text.snippet',
 'uuid': 'C611D263-828B-4B18-8844-E6F0BE2BF7F1'}

#Snippet nodes
class Node(object):
    child_nodelists = ('nodelist',)

    def render(self, context):
        "Return the node rendered as a string"
        pass

    def __iter__(self):
        yield self

    def get_nodes_by_type(self, nodetype):
        "Return a list of all nodes (within this node and its nodelist) of the given type"
        nodes = []
        if isinstance(self, nodetype):
            nodes.append(self)
        for attr in self.child_nodelists:
            nodelist = getattr(self, attr, None)
            if nodelist:
                nodes.extend(nodelist.get_nodes_by_type(nodetype))
        return nodes

class NodeList(list):
    # Set to True the first time a non-TextNode is inserted by
    # extend_nodelist().
    contains_nontext = False

    def render(self, context):
        bits = []
        for node in self:
            if isinstance(node, Node):
                bits.append(self.render_node(node, context))
            else:
                bits.append(node)
        return mark_safe(''.join([force_unicode(b) for b in bits]))

    def get_nodes_by_type(self, nodetype):
        "Return a list of all nodes of the given type"
        nodes = []
        for node in self:
            nodes.extend(node.get_nodes_by_type(nodetype))
        return nodes

    def render_node(self, node, context):
        return node.render(context)

class TextNode(Node):
    def __init__(self, s):
        self.s = s

    def __repr__(self):
        return "<Text Node: '%s'>" % smart_str(self.s[:25], 'ascii', errors='replace')

    def render(self, context):
        return self.s

class PMXSnippetProcessor(PMXSyntaxProcessor):
    def __init__(self):
        pass
        
    def open_tag(self, name, start):
        pass

    def close_tag(self, name, end):
        pass

    def new_line(self, line):
        pass

    def start_parsing(self, name):
        pass

    def end_parsing(self, name):
        pass

class PMXSnippet(PMXBundleItem):
    parser = PMXSyntax(SNIPPET_SYNTAX)
    def __init__(self, hash, name_space = "default"):
        super(PMXSnippet, self).__init__(hash, name_space)
        for key in [    'content', 'disableAutoIndent', 'inputPattern', 'bundlePath' ]:
            setattr(self, key, hash.pop(key, None))
    
    def compile(self):
        processor = PMXDebugSyntaxProcessor()
        self.parser.parse(self.content, processor)
        text = self.content.splitlines()
