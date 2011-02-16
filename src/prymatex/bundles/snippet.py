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
 'patterns': [{'captures': {'1': {'name': 'keyword.escape.snippet'}},
               'match': '\\\\(\\\\|\\$|`)',
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
               'name': 'meta.structure.variable.snippet',
               'patterns': [{'include': '#escaped_char'},
                            {'include': '#substitution'}]},
              {'begin': '`',
               'end': '`',
               'contentName': 'string.script',
               'name': 'string.interpolated.shell.snippet'}],
 'repository': {'condition': {'begin': '\\(\\?(\\d):',
                              'beginCaptures': {'1': {'name': 'string.regexp.condition'}},
                              'contentName': 'text.condition',
                              'end': '\\)',
                              'name': 'meta.structure.condition.regexp',
                              'patterns': [#{'include': '#replacements'},
                                           {'begin': ':',
                                            'end': '(?=\\))',
                                            'name': 'meta.structure.condition.regexp',
                                            #'patterns': [{'include': '#replacements'}]
                                            }]},
                'escaped_char': {'match': '\\\\[/\\\\]',
                                 'name': 'constant.character.escape.regexp'},
                #'replacements': {'match': '\\$\\d|\\\\[uUILE]',
                #                 'name': 'string.regexp.replacement'},
                'substitution': {'begin': '/',
                                 'contentName': 'string.regexp.format',
                                 'end': '/([mg]?)',
                                 'endCaptures': {'1': {'name': 'string.regexp.options'}},
                                 'patterns': [{'include': '#escaped_char'},
                                              {'include': '#condition'}]}},
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
    
    def __len__(self):
        return reduce(lambda x, y: x + y, map(lambda e: len(e), self.children), 0)
    
    def append(self, element):
        if isinstance(element, (str, unicode)):
            element = element.replace('\\n', '\n').replace('\\t', '\t')
        self.children.append(element)
    
    def clear(self):
        self.children = []
    
    def position(self, element, index):
        for child in self.children:
            if child == element:
                break;
            if isinstance(child, (str, unicode)):
                if '\n' in child:
                    index = ( index[0] + len(child.split('\n')) - 1, len(child.split('\n')[-1]) )
                else:
                    index = ( index[0], index[1] + len(child) )
            else:
                index = child.position(element, index)
        return index
    
    def resolve(self, indentation, tabreplacement, environment):
        for index in xrange(len(self.children)):
            if isinstance(self.children[index], (str, unicode)):
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
        else:
            print "Snippet open", name, text
        return node
        
    def close(self, name, text):
        self.append(text)
        print "Snippet close", name, text
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
        print "Tabstop open", name, text
        return node
        
    def close(self, name, text):
        if name == 'meta.structure.tabstop.snippet':
            return self.parent
        elif name == 'keyword.tabstop.snippet':
            self.index = int(text)
        else:
            print "Tabstop close", name, text
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
        self.placeholder = None
        
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

    def __str__(self):
        if self.placeholder != None:
            return str(self.placeholder)
        return super(Placeholder, self).__str__()
    
    def __len__(self):
        return len(str(self))
    
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
        elif name == 'meta.structure.variable.snippet':
            node = Variable(self)
            self.append(node)
        else:
            print "Placeholder open", name, text
        return node

    def close(self, name, text):
        if name == 'meta.structure.placeholder.snippet':
            return self.parent
        elif name == 'keyword.placeholder.snippet':
            self.index = int(text)
        elif name == 'string.default':
            self.append(text)
        else:
            print "Placeholder close", name, text
        return self

    def taborder(self, container):
        if isinstance(container, list) and container:
            for element in container:
                element.placeholder = self
        elif isinstance(container, Placeholder):
            self.placeholder = container
            return container
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
        node.regexp = deepcopy(self.regexp, memo)
        container = memo["taborder"].setdefault(node.index, [])
        if (node != container and node not in container):
            memo["taborder"][node.index] = node.taborder(container)
        return node
        
    def __len__(self):
        return len(str(self))

    def position(self, element, index):
        value = str(self)
        if '\n' in value:
            index = ( index[0] + len(value.split('\n')) - 1, len(value.split('\n')[-1]) )
        else:
            index = ( index[0], index[1] + len(value) )
        return index
        
    def open(self, name, text):
        node = self
        if name == 'string.regexp':
            node = self.regexp = Regexp(self)
        else:
            print "Transformation open", name, text
        return node
        
    def close(self, name, text):
        if name == 'meta.structure.transformation.snippet':
            return self.parent
        elif name == 'keyword.transformation.snippet':
            self.index = int(text)
        else:
            print "Transformation close", name, text
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
        node.regexp = deepcopy(self.regexp, memo)
        return node

    def __str__(self):
        text = "".join(self.children)
        if self.regexp != None:
            return "".join(self.regexp.transform(text))
        else:
            return text
            
    def position(self, element, index):
        value = str(self)
        if '\n' in value:
            index = ( index[0] + len(value.split('\n')) - 1, len(value.split('\n')[-1]))
        else:
            index = ( index[0], index[1] + len(value))
        return index
        
    def open(self, name, text):
        node = self
        if name == 'string.regexp':
            node = self.regexp = Regexp(self)
        else:
            print "Variable, open", name, text
        return node

    def close(self, name, text):
        if name == 'meta.structure.variable.snippet':
            return self.parent
        elif name == 'string.env.snippet':
            self.name = text
        elif name == 'string.default':
            self.append(text)
        else:
            print "no, tratado", name, text
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
        self.pattern = ""
        self.options = None

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
            self.pattern += text[:-1];
            self.pattern = onig_compile(self.pattern)
        elif name == 'meta.structure.condition.regexp':
            self.append(text.replace('\\n', '\n').replace('\\t', '\t'))
            node = Condition(self)
            self.append(node)
        elif name == 'constant.character.escape.regexp':
            #Escape in pattern
            if isinstance(self.pattern, (str, unicode)):
                self.pattern += text
            else:
                self.append(text.replace('\\n', '\n').replace('\\t', '\t'))
        else:
            print "Regexp open", name, text
        return node

    def close(self, name, text):
        if name == 'string.regexp':
            return self.parent
        elif name == 'string.regexp.format':
            self.append(text.replace('\\n', '\n').replace('\\t', '\t'))
        elif name == 'string.regexp.options':
            self.options = text
        elif name == 'constant.character.escape.regexp':
            #Escape in pattern
            if isinstance(self.pattern, (str, unicode)):
                self.pattern += text
            else:
                self.append(text.replace('\\n', '\n').replace('\\t', '\t'))
        else:
            print "Regexp close", name, text
        return self

    def transform(self, text):
        result = ""
        for child in self.children:
            matches = self.pattern.find(text)
            for match in matches:
                if isinstance(child, (str, unicode)):
                    result += self.substitute(child, match)
                else:
                    result += child.substitute(match)
                if self.options == None or 'g' not in self.options:
                    break;
        return result
        
    def substitute(self, string, match):
        values = onig_compile("\$(\d+)").split(string)
        for index in xrange(1, len(values), 2):
            values[index] = match[index]
        return "".join(values)
    
class Shell(Node):
    def open(self, name, text):
        node = self
        if name == 'string.script':
            self.append(text[1:])
        else:
            print "Shell open", name, text
        return node
        
    def close(self, name, text):
        if name == 'string.interpolated.shell.snippet':
            return self.parent
        elif name == 'string.script':
            self.append(text)
        else:
            print "Shell close", name, text
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
        self.format = ""

    def __deepcopy__(self, memo):
        node = Condition(memo["parent"])
        node.index = self.index
        node.format = self.format
        return node

    def open(self, name, text):
        node = self
        print "Condition open", name, text
        return node
        
    def close(self, name, text):
        if name == 'meta.structure.condition.regexp':
            return self.parent
        elif name == 'string.regexp.condition':
            self.index = int(text)
        elif name == 'text.condition':
            self.format += text.replace('\\n', '\n').replace('\\t', '\t')
        else:
            print "Condition close", name, text
        return self
    
    def substitute(self, match):
        if match and match[self.index] != None:
            values = onig_compile("\$(\d+)").split(self.format)
            for index in xrange(1, len(values), 2):
                values[index] = match[int(values[index])]
            return "".join(values)
        return ""
            
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
        self.index = 0
        self.starts = (0, 0)
        
    def __deepcopy__(self, memo):
        snippet = PMXSnippet(self.hash, self.name_space)
        memo["snippet"] = deepcopy(self.snippet, memo)
        return snippet
    
    def __str__(self):
        return str(self.snippet)
    
    def __unicode__(self):
        return unicode(self.snippet)
    
    def __len__(self):
        return len(self.snippet)
    
    @property
    def ends(self):
        return self.position(None)
    
    def clone(self):
        memo = {"parent": None, "snippet": None, "taborder": {}}
        new = deepcopy(self, memo)
        new.snippet = memo["snippet"]
        new.addTaborder(memo["taborder"])
        return new
    
    def ready(self):
        return self.snippet != None
    
    def compile(self):
        processor = PMXSnippetProcessor()
        self.parser.parse(self.content, processor)
        self.snippet = processor.node
        self.addTaborder(processor.taborder)
    
    def addTaborder(self, taborder):
        self.taborder = []
        last = taborder.pop(0, None)
        keys = taborder.keys()
        keys.sort()
        for key in keys:
            self.taborder.append(taborder.pop(key))
        self.taborder.append(last)

    def getHolder(self, index):
        ''' Return the placeholder for index, where index = (row, column)'''
        for holder in self.taborder:
            # if holder == None then is the end of taborders
            if holder == None: return None
            holder_index = self.position(holder)
            if holder_index[0] == index[0] and holder_index[1] <= index[1] < holder_index[1] + len(holder):
                return holder
        return None
    
    def setCurrentHolder(self, holder):
        self.index = self.taborder.index(holder)
    
    def current(self):
        return self.taborder[self.index]

    def next(self):
        if self.index < len(self.taborder) - 1:
            self.index += 1
        return self.taborder[self.index]

    def previous(self):
        if self.index > 0:
            self.index -= 1
        return self.taborder[self.index]
    
    def position(self, tabstop):
        return self.snippet.position(tabstop, self.starts)
    
    def resolve(self, indentation, tabreplacement, starts, environment):
        self.starts = starts
        self.snippet.resolve(indentation, tabreplacement, environment)
    
    def write(self, index, text):
        if index < len(self.taborder) and self.taborder[index] != None and hasattr(self.taborder[index], "write"):
            self.taborder[index].write(text)