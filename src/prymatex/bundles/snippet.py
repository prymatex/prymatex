#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    Snippte's module
'''
import os, stat, tempfile
from copy import deepcopy
from subprocess import Popen, PIPE, STDOUT
import ponyguruma as onig
from ponyguruma.constants import OPTION_CAPTURE_GROUP, SYNTAX_RUBY

onig_compile = onig.Regexp.factory(flags = OPTION_CAPTURE_GROUP)

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
               'patterns': [{'include': '#substitution'}]},
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
               'name': 'meta.structure.variable.snippet',
               'patterns': [{'include': '#substitution'}]},
              {'begin': '`',
               'end': '`',
               'contentName': 'string.script',
               'name': 'string.interpolated.shell.snippet'}],
 'repository': {'condition': {'begin': '\\(\\?(\\d):',
                              'beginCaptures': {'1': {'name': 'string.regexp.condition'}},
                              'contentName': 'text.condition',
                              'end': '\\)',
                              'name': 'meta.structure.condition.regexp'},
                'substitution': {'begin': '/',
                                 'contentName': 'string.regexp.format',
                                 'end': '/([mg]?)',
                                 'endCaptures': {'1': {'name': 'string.regexp.options'}},
                                 'patterns': [{'include': '#condition'}]}},
}

#Snippet nodes
class Node(object):
    def __init__(self, parent = None):
        self.parent = parent
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
            return False
        else:
            return element in self.children
    
    def __len__(self):
        return reduce(lambda x, y: x + y, map(lambda e: len(e), self.children), 0)
    
    def append(self, element):
        if type(element) == str:
            element = element.replace('\\n', '\n').replace('\\t', '\t')
        self.children.append(element)
    
    def clear(self):
        self.children = []
    
    def position(self, element):
        index = (0, 0)
        for child in self.children:
            if child == element:
                break;
            if '\n' in child:
                index = ( 0, index[1] + 1 )
            else:
                index = ( index[0] + len(child), index[1] )
        return index
    
    def resolve(self, indentation, tabreplacement, environment):
        for index in xrange(len(self.children)):
            if type(self.children[index]) == str:
                self.children[index] = self.children[index].replace('\n', '\n' + indentation).replace('\t', tabreplacement)
            else:
                self.children[index].resolve(indentation, tabreplacement, environment)

    def open(self, name, text):
        pass

    def close(self, name, text):
        pass
    
class Snippet(Node):
    def __deepcopy__(self, memo):
        node = Snippet(memo["parent"])
        memo["parent"] = node
        for child in self.children:
            if isinstance(child, Node):
                node.append(deepcopy(child, memo))
            else:
                node.append(child)
        return node
        
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
        elif name == 'string.interpolated.shell.snippet':
            node = Shell(self)
            self.append(node)
        if node == None:
            print "no puedo con %s" % name
        return node
        
    def close(self, name, text):
        self.append(text)
        return self

class Tabstop(Node):
    def __init__(self, parent = None):
        super(Tabstop, self).__init__(parent)
        self.placeholder = None
        self.index = None
        
    def __str__(self):
        if self.placeholder != None:
            return str(self.placeholder)
        else:
            return ""

    def __deepcopy__(self, memo):
        node = Tabstop(memo["parent"])
        memo["parent"] = node
        for child in self.children:
            if isinstance(child, Node):
                node.append(deepcopy(child, memo))
            else:
                node.append(child)
        node.index = self.index
        container = memo["taborder"].setdefault(node.index, [])
        if (node != container and node not in container):
            memo["taborder"][node.index] = node.taborder(container)
        return node
        
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
        self.index = None
        
    def __deepcopy__(self, memo):
        node = Placeholder(memo["parent"])
        memo["parent"] = node
        for child in self.children:
            if isinstance(child, Node):
                node.append(deepcopy(child, memo))
            else:
                node.append(child)
        node.index = self.index
        container = memo["taborder"].setdefault(node.index, [])
        if (node != container and node not in container):
            memo["taborder"][node.index] = node.taborder(container)
        return node
        
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
        self.index = None
        self.regexp = None
    
    def __str__(self):
        text = ""
        if self.placeholder != None:
            text = str(self.placeholder)
        return "".join(self.regexp.transform(text))

    def __deepcopy__(self, memo):
        node = Transformation(memo["parent"])
        memo["parent"] = node
        for child in self.children:
            if isinstance(child, Node):
                node.append(deepcopy(child, memo))
            else:
                node.append(child)
        node.index = self.index
        node.regexp = self.regexp
        container = memo["taborder"].setdefault(node.index, [])
        if (node != container and node not in container):
            memo["taborder"][node.index] = node.taborder(container)
        return node
        
    def __len__(self):
        return len(str(self))
    
    def open(self, name, text):
        node = self
        if name == 'string.regexp':
            node = self.regexp = Regexp(self)
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
        
    def resolve(self, indentation, tabreplacement, environment):
        if self.regexp != None:
            self.regexp.resolve(indentation, tabreplacement, environment)    
        
class Variable(Node):
    def __init__(self, parent = None):
        super(Variable, self).__init__(parent)
        self.name = None
        self.regexp = None

    def __deepcopy__(self, memo):
        node = Variable(memo["parent"])
        memo["parent"] = node
        for child in self.children:
            if isinstance(child, Node):
                node.append(deepcopy(child, memo))
            else:
                node.append(child)
        node.name = self.name
        node.regexp = self.regexp
        return node

    def __str__(self):
        text = "".join(self.children)
        if self.regexp != None:
            return "".join(self.regexp.transform(text))
        else:
            return text

    def open(self, name, text):
        node = self
        if name == 'string.regexp':
            node = self.regexp = Regexp(self)
            self.append(node)
        return node

    def close(self, name, text):
        if name == 'meta.structure.variable.snippet':
            return self.parent
        elif name == 'string.env.snippet':
            self.name = text
        elif name == 'string.default':
            self.append(text)
        return self
    
    def resolve(self, indentation, tabreplacement, environment):
        if self.name in environment:
            self.clear()
            self.append(environment[self.name])
        if self.regexp != None:
            self.regexp.resolve(indentation, tabreplacement, environment)
        
class Regexp(Node):
    def __init__(self, parent = None):
        super(Regexp, self).__init__(parent)
        self.pattern = None
        self.format = None
        self.options = None
        self.condition = None

    def __str__(self):
        return "%s/%s/%s" % (self.pattern, self.format, self.options)

    def __deepcopy__(self, memo):
        node = Regexp(memo["parent"])
        memo["parent"] = node
        for child in self.children:
            if isinstance(child, Node):
                node.append(deepcopy(child, memo))
            else:
                node.append(child)
        node.pattern = self.pattern
        node.options = self.options
        return node
        
    def open(self, name, text):
        node = self
        if name == 'string.regexp.format':
            self.pattern = onig_compile(text[:-1])
        elif name == 'meta.structure.condition.regexp':
            node = Condition(self)
            self.append(node)
        return node

    def close(self, name, text):
        if name == 'string.regexp':
            return self.parent
        elif name == 'string.regexp.format' and text:
            self.append(text.replace('\\n', '\n').replace('\\t', '\t'))
        elif name == 'string.regexp.options':
            self.options = text
        return self

    def transform(self, text):
        text = ""
        for child in self.children:
            match = self.pattern.search(text)
            if type(child) == str:
                text += self.substitute(child, match)
            else:
                text += self.pattern.sub(child.substitute, text)
                #return self.pattern.sub(lambda match: self.format.replace("$%d" % self.condition, match[self.condition]), text)
        return text
        
    def substitute(self, string, match):
        values = onig_compile("\$(\d+)").split(string)
        for index in xrange(len(values), 1):
            values[index] = match[index]
        return "".join(values)
    
class Shell(Node):
    def open(self, name, text):
        node = self
        if name == 'string.script':
            self.append(text[1:])
        return node
        
    def close(self, name, text):
        if name == 'string.interpolated.shell.snippet':
            return self.parent
        elif name == 'string.script':
            self.append(text)
        return self

    def resolve(self, indentation, tabreplacement, environment):
        descriptor, name = tempfile.mkstemp(prefix='pmx')
        os.write(descriptor, str(self).encode('utf8'))
        os.chmod(name, stat.S_IEXEC)
        process = Popen([name], stdout=PIPE, stderr=STDOUT, env = environment)
        self.clear()
        result = process.stdout.read()
        self.append(result.strip())
        process.stdout.close()

class Condition(Node):
    def __init__(self, parent = None):
        super(Condition, self).__init__(parent)
        self.index = None
        self.format = None
        
    def open(self, name, text):
        node = self
        return node
        
    def close(self, name, text):
        if name == 'meta.structure.condition.regexp':
            return self.parent
        elif name == 'string.regexp.condition':
            self.index = int(text)
        elif name == 'text.condition':
            self.format = text.replace('\\n', '\n').replace('\\t', '\t')
        return self
    
    def substitute(self, match):
        if match:
            print repr(match[0])
        values = onig_compile("\$(\d+)").split(self.format)
        if match and match.groups[self.index]:
            print match.groups[self.index]
            for index in xrange(len(values), 1):
                print values[index]
                values[index] = match[index]
        return "".join(values)
            
    def resolve(self, indentation, tabreplacement, environment):
        self.format = self.format.replace('\n', '\n' + indentation).replace('\t', tabreplacement)

class PMXSnippetProcessor(PMXSyntaxProcessor):
    def __init__(self):
        self.current = None
        self.node = Snippet()
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
        if self.current != None:
            if self.index != len(self.current):
                self.node.append(self.current[self.index:len(self.current)])
            self.node.append("\n")
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
        self.snippet = None
        self.taborder = None
        self.index = 1
        
    def __deepcopy__(self, memo):
        snippet = PMXSnippet(self.hash, self.name_space)
        memo["snippet"] = deepcopy(self.snippet, memo)
        return snippet
    
    def __str__(self):
        return str(self.snippet)
    
    def __len__(self):
        return len(self.snippet)
    
    def current(self):
        if self.index > len(self.taborder) - 1:
            return 0 in self.taborder and self.taborder[0] or None
        else:
            return self.taborder[self.index]
        
    def next(self):
        if self.index >= len(self.taborder) - 1:
            return 0 in self.taborder and self.taborder[0] or None
        else:
            self.index += 1
            return self.taborder[self.index]
        
    def previous(self):
        if self.index < 1:
            return self.taborder[1]
        else:
            self.index -= 1
            return self.taborder[self.index]
    
    def position(self, tabstop):
        return self.snippet.position(tabstop)
        
    def clone(self):
        memo = {"parent": None, "snippet": None, "taborder": {}}
        new = deepcopy(self, memo)
        new.snippet = memo["snippet"]
        new.taborder = memo["taborder"]
        return new
    
    def resolve(self, indentation, tabreplacement, environment):
        self.snippet.resolve(indentation, tabreplacement, environment)
    
    def compile(self):
        text = self.content.splitlines()
        processor = PMXDebugSyntaxProcessor()
        processor = PMXSnippetProcessor()
        self.parser.parse(self.content, processor)
        self.snippet = processor.node
        self.taborder = processor.taborder
    
    def write(self, index, text):
        if index in self.taborder:
            self.taborder[index].write(text)