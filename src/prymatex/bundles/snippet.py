#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    Snippte's module
'''

if __name__ == "__main__":
    from syntax import PMXSyntax
    from processor import PMXDebugSyntaxProcessor
else:
    from prymatex.bundles.syntax import PMXSyntax
    from prymatex.bundles.processor import PMXDebugSyntaxProcessor

PMX_SNIPPETS = {}

SNIPPET_SYNTAX = {'name': 'Snippet',
'patterns': [{'match': '\\\\(\\\\|\\$|`)',
              'name': 'constant.character.escape.snippet'},
             {'captures': {'1': {'name': 'entity.name.function.snippet'},
                           '2': {'name': 'keyword.tabstop.snippet'}},
              'match': '(\\$)(\\d+)',
              'name': 'meta.structure.tabstop.snippet'},
             {'begin': '(\\$\\{)(\\d+)(:)',
              'beginCaptures': {'1': {'name': 'entity.name.function.snippet'},
                                '2': {'name': 'keyword.tabstop.snippet'},
                                '3': {'name': 'entity.name.function.snippet'}},
              'end': '\\}',
              'endCaptures': {'0': {'name': 'entity.name.function.snippet'}},
              'name': 'meta.structure.tabstop.snippet',
              'patterns': [{'include': '$self'}]},
             {'begin': '(\\$\\{)(\\d+)(/)',
              'beginCaptures': {'1': {'name': 'entity.name.function.snippet'},
                                '2': {'name': 'keyword.tabstop.snippet'},
                                '3': {'name': 'entity.name.function.snippet'}},
              'contentName': 'string.regexp',
              'end': '\\}',
              'endCaptures': {'0': {'name': 'entity.name.function.snippet'}},
              'name': 'meta.structure.tabstop.snippet',
              'patterns': [{'include': '#escaped_char'},
                           {'include': '#substitution'}]},
             {'captures': {'1': {'name': 'entity.name.function.snippet'},
                           '2': {'name': 'string.env.snippet'}},
              'match': '(\\$)([a-zA-Z_][a-zA-Z0-9_]*)',
              'name': 'meta.structure.variable.snippet'},
             {'begin': '(\\$\\{)([a-zA-Z_][a-zA-Z0-9_]*)(:)',
              'beginCaptures': {'1': {'name': 'entity.name.function.snippet'},
                                '2': {'name': 'string.env.snippet'},
                                '3': {'name': 'entity.name.function.snippet'}},
              'end': '\\}',
              'endCaptures': {'0': {'name': 'entity.name.function.snippet'}},
              'name': 'meta.structure.variable.snippet',
              'patterns': [{'include': '$self'}]},
             {'begin': '(\\$\\{)([a-zA-Z_][a-zA-Z0-9_]*)(/)',
              'beginCaptures': {'1': {'name': 'entity.name.function.snippet'},
                                '2': {'name': 'string.env.snippet'},
                                '3': {'name': 'entity.name.function.snippet'}},
              'contentName': 'string.regexp',
              'end': '\\}',
              'endCaptures': {'0': {'name': 'entity.name.function.snippet'}},
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
'scopeName': 'text.snippet'}

parser = PMXSyntax(SNIPPET_SYNTAX, None)

class PMXSnippet(object):
    def __init__(self, hash, name_space = 'default'):
        
        self.name_space = name_space
        for key in [    'name', 'content', 'scope', 'tabTrigger', 'keyEquivalent', 'disableAutoIndent', 'inputPattern', 'bundlePath' ]:
            setattr(self, key, hash.pop(key, None))
        
        PMX_SNIPPETS.setdefault(self.name_space, {})

def parse_file(filename):
    import plistlib
    data = plistlib.readPlist(filename)
    return PMXSnippet(data)

if __name__ == '__main__':
    import os
    from glob import glob
    files = glob(os.path.join('../share/Bundles/', '*'))
    for f in files:
        snippets = glob(os.path.join(f, 'Snippets/*'))
        for s in snippets:
            try:
                snippet = parse_file(s)
                parser.parse(snippet.content, PMXDebugSyntaxProcessor())
            except Exception, e:
                print "Error in %s, %s" % (s, e)