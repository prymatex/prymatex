#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    Snippte's module
'''
import os, stat, tempfile, logging
from copy import deepcopy
from subprocess import Popen, PIPE, STDOUT
import ponyguruma as onig
from ponyguruma.constants import OPTION_CAPTURE_GROUP
from prymatex.bundles.base import PMXBundleItem
from prymatex.bundles.processor import PMXSyntaxProcessor
from prymatex.bundles.syntax import PMXSyntax

logger = logging.getLogger(__name__)
onig_compile = onig.Regexp.factory(flags = OPTION_CAPTURE_GROUP)

SNIPPET_SYNTAX = {
 'patterns': [{'captures': {'1': {'name': 'keyword.escape.snippet'}},
               'match': '\\\\(\\\\|\\$|`)',
               'name': 'constant.character.escape.snippet'},
              #Structures
              #TabStop
              {'captures': {'1': {'name': 'keyword.tabstop.snippet'}},
               'match': '\\$(\\d+)|\\${(\\d+)}',
               'name': 'structure.tabstop.snippet'},
              #Placeholder
              {'begin': '\\$\\{(\\d+):',
               'beginCaptures': {'1': {'name': 'keyword.placeholder.snippet'}},
               'contentName': 'string.default',
               'end': '\\}',
               'name': 'structure.placeholder.snippet',
               'patterns': [{'include': '$self'}]},
              #Transformation
              {'begin': '\\$\\{(\\d+)/',
               'beginCaptures': {'1': {'name': 'keyword.transformation.snippet'}},
               'contentName': 'string.regexp',
               'end': '\\}',
               'name': 'structure.transformation.snippet',
               'patterns': [{'include': '#escaped_char'},
                            {'include': '#substitution'}]},
              # Variables
              #TabStop
              {'match': '\\$([a-zA-Z_][a-zA-Z0-9_]*)|\\${([a-zA-Z_][a-zA-Z0-9_]*)}',
               'captures': {'1': {'name': 'string.env.snippet'}},
               'name': 'variable.tabstop.snippet'},
              #Placeholder
              {'begin': '\\$\\{([a-zA-Z_][a-zA-Z0-9_]*):',
               'beginCaptures': {'1': {'name': 'string.env.snippet'}},
               'contentName': 'string.default',
               'end': '\\}',
               'name': 'variable.placeholder.snippet',
               'patterns': [{'include': '$self'}]},
              #Transformation
              {'begin': '\\$\\{([a-zA-Z_][a-zA-Z0-9_]*)/',
               'beginCaptures': {'1': {'name': 'string.env.snippet'}},
               'contentName': 'string.regexp',
               'end': '\\}',
               'name': 'variable.transformation.snippet',
               'patterns': [{'include': '#escaped_char'},
                            {'include': '#substitution'}]},
               #Shell
              {'begin': '`',
               'end': '`',
               'contentName': 'string.script',
               'name': 'string.interpolated.shell.snippet'}],
 'repository': {'condition': {'begin': '\\(\\?(\\d):',
                              'beginCaptures': {'1': {'name': 'string.regexp.condition'}},
                              'contentName': 'text.condition',
                              'end': '\\)',
                              'name': 'meta.structure.condition.regexp',
                              'patterns': [{'include': '#escaped_cond'},
                                           {'begin': ':',
                                            'end': '(?=\\))',
                                            'contentName': 'otherwise.condition',
                                            'patterns': [{'include': '#escaped_cond'}]
                                            }]},
                'escaped_cond': {'captures': {'1': {'name': 'keyword.escape.condition'}},
                                 'match': '\\\\(\\))',
                                 'name': 'constant.character.escape.condition'},
                'escaped_char': {'match': '\\\\[/\\\\\\}\\{]',
                                 'name': 'constant.character.escape.regexp'},
                #'replacements': {'match': '\\$\\d|\\\\[uUILE]',
                #                 'name': 'string.regexp.replacement'},
                'substitution': {'begin': '/',
                                 'contentName': 'string.regexp.format',
                                 'end': '/([mg]?)/?',
                                 'endCaptures': {'1': {'name': 'string.regexp.options'}},
                                 'patterns': [{'include': '#escaped_char'},
                                              {'include': '#condition'}]}},
}

#Snippet Node Bases
class Node(object):
    def __init__(self, scope, parent = None):
        self.parent = parent
        self.scope = scope

    def __len__(self):
        return len(str(self))

    def resolve(self, indentation, tabreplacement, environment):
        pass

    def open(self, scope, text):
        logger.debug("%s open %s %s" % (self.__class__.__name__, scope, text))
        return self

    def close(self, scope, text):
        if scope == self.scope:
            return self.parent
        else:
            logger.debug("%s close %s %s" % (self.__class__.__name__, scope, text))
        return self

class TextNode(Node):
    def __init__(self, text, parent = None):
        super(TextNode, self).__init__("string", parent)
        self.text = text.replace('\\n', '\n').replace('\\t', '\t')

    def __str__(self):
        return self.text

    def __deepcopy__(self, memo):
        return TextNode(self.text, memo["parent"])
        
    def resolve(self, indentation, tabreplacement, environment):
        self.text = self.text.replace('\n', '\n' + indentation).replace('\t', tabreplacement)

class NodeList(list):
    def __init__(self, scope, parent = None):
        super(NodeList, self).__init__()
        self.parent = parent
        self.scope = scope

    def __str__(self):
        string = ""
        for child in self:
            string += str(child)
        return string
    
    def __len__(self):
        return len(str(self))
    
    def __contains__(self, element):
        for child in self:
            if child == element:
                return True
            elif isinstance(child, NodeList) and element in child:
                return True
        return False
    
    def append(self, element):
        if isinstance(element, (str, unicode)):
            element = TextNode(element, self)
        super(NodeList, self).append(element)
    
    def clear(self):
        while self:
            self.pop()
    
    def resolve(self, indentation, tabreplacement, environment):
        for child in self:
            child.resolve(indentation, tabreplacement, environment)

    def open(self, scope, text):
        if scope == 'constant.character.escape.snippet':
            self.append(text)
        else:
            logger.debug("%s open %s %s" % (self.__class__.__name__, scope, text))
        return self

    def close(self, scope, text):
        if scope == self.scope:
            return self.parent
        elif scope == 'keyword.escape.snippet':
            self.append(text)
        else:
            self.append(text)
            logger.debug("%s close %s %s" % (self.__class__.__name__, scope, text))
        return self
    
#Snippet root
class Snippet(NodeList):
    def __init__(self, scope, parent = None):
        super(Snippet, self).__init__(scope, parent)
        self.__starts = None
        self.__ends = None
    
    def __deepcopy__(self, memo):
        node = Snippet(self.scope, memo["parent"])
        memo["parent"] = node
        for child in self:
            node.append(deepcopy(child, memo))
        return node
    
    def setStarts(self, value):
        self.__starts = value
        
    def getStarts(self):
        return (self.__starts != None) and self.__starts or 0
    
    starts = property(getStarts, setStarts)
    
    def setEnds(self, value):
        self.__ends = value
        
    def getEnds(self):
        return (self.__ends != None) and self.__ends or len(self)
    
    ends = property(getEnds, setEnds)
        
    def open(self, scope, text):
        node = self
        if scope == 'structure.tabstop.snippet':
            self.append(text)
            node = StructureTabstop(scope, self)
            self.append(node)
        elif scope == 'structure.placeholder.snippet':
            self.append(text)
            node = StructurePlaceholder(scope, self)
            self.append(node)
        elif scope == 'structure.transformation.snippet':
            self.append(text)
            node = StructureTransformation(scope, self)
            self.append(node)
        elif scope == 'variable.tabstop.snippet':
            self.append(text)
            node = VariableTabstop(scope, self)
            self.append(node)
        elif scope == 'variable.placeholder.snippet':
            self.append(text)
            node = VariablePlaceholder(scope, self)
            self.append(node)
        elif scope == 'variable.transformation.snippet':
            self.append(text)
            node = VariableTransformation(scope, self)
            self.append(node)
        elif scope == 'string.interpolated.shell.snippet':
            self.append(text)
            node = Shell(scope, self)
            self.append(node)
        else:
            return super(Snippet, self).open(scope, text)
        return node
        
    def position(self, element):
        pos = self.starts
        def index(holder, element):
            val = 0
            for child in holder:
                if child == element:
                    break
                elif isinstance(child, Snippet) and element in child:
                    val += index(child, element)
                    break
                else:
                    val += len(child)
            return val
        return pos + index(self, element)

#Snippet structures
class StructureTabstop(Node):
    def __init__(self, scope, parent = None):
        super(StructureTabstop, self).__init__(scope, parent)
        self.placeholder = None
        self.index = None
        self.content = ""

    def __str__(self):
        if self.placeholder != None:
            return str(self.placeholder)
        else:
            return self.content

    def __deepcopy__(self, memo):
        node = StructureTabstop(self.scope, memo["parent"])
        node.index = self.index
        container = memo["taborder"].setdefault(node.index, [])
        if (node != container and node not in container):
            memo["taborder"][node.index] = node.taborder(container)
        return node
        
    def close(self, scope, text):
        node = self
        if scope == 'keyword.tabstop.snippet':
            self.index = int(text)
        else:
            return super(StructureTabstop, self).close(scope, text)
        return node

    def position(self):
        root = self.parent
        while (root.parent != None):
            root = root.parent
        return root.position(self)
    
    def taborder(self, container):
        if type(container) == list:
            container.append(self)
        else:
            self.placeholder = container
        return container
        
    def insert(self, character, position):
        text = str(self)
        text = text[:position] + character + text[position:]
        self.content = text
    
    def remove(self, start, end = None):
        end = end != None and end or start
        text = str(self)
        text = text[:start] + text[end:]
        self.content = text
    
    def clear(self):
        self.content = ""
    
class StructurePlaceholder(Snippet):
    def __init__(self, scope, parent = None):
        super(StructurePlaceholder, self).__init__(scope, parent)
        self.index = None
        self.placeholder = None
        
    def __deepcopy__(self, memo):
        node = StructurePlaceholder(self.scope, memo["parent"])
        memo["parent"] = node
        for child in self:
            node.append(deepcopy(child, memo))
        node.index = self.index
        container = memo["taborder"].setdefault(node.index, [])
        if (node != container and node not in container):
            memo["taborder"][node.index] = node.taborder(container)
        return node

    def __str__(self):
        if self.placeholder != None:
            return str(self.placeholder)
        return super(StructurePlaceholder, self).__str__()
    
    def close(self, scope, text):
        node = self
        if scope == 'keyword.placeholder.snippet':
            self.index = int(text)
        else:
            return super(StructurePlaceholder, self).close(scope, text)
        return node

    def taborder(self, container):
        if type(container) == list and container:
            for element in container:
                element.placeholder = self
        elif isinstance(container, StructurePlaceholder):
            self.placeholder = container
            return container
        return self

    def position(self):
        root = self.parent
        while (root.parent != None):
            root = root.parent
        return root.position(self)
    
    def insert(self, character, position):
        text = str(self)
        text = text[:position] + character + text[position:]
        self.clear()
        self.append(text)
    
    def remove(self, start, end = None):
        end = end != None and end or start
        text = str(self)
        text = text[:start] + text[end:]
        self.clear()
        self.append(text)
        
class StructureTransformation(Node):
    def __init__(self, scope, parent = None):
        super(StructureTransformation, self).__init__(scope, parent)
        self.placeholder = None
        self.index = None
        self.regexp = None
    
    def __str__(self):
        text = ""
        if self.placeholder != None:
            text = str(self.placeholder)
        return "".join(self.regexp.transform(text))

    def __deepcopy__(self, memo):
        node = StructureTransformation(self.scope, memo["parent"])
        memo["parent"] = node
        node.index = self.index
        node.regexp = deepcopy(self.regexp, memo)
        container = memo["taborder"].setdefault(node.index, [])
        if (node != container and node not in container):
            memo["taborder"][node.index] = node.taborder(container)
        return node
        
    def open(self, scope, text):
        node = self
        if scope == 'string.regexp':
            node = self.regexp = Regexp(scope, self)
        else:
            return super(StructureTransformation, self).open(scope, text)
        return node
        
    def close(self, scope, text):
        node = self
        if scope == 'keyword.transformation.snippet':
            self.index = int(text)
        else:
            return super(StructureTransformation, self).close(scope, text)
        return node
    
    def taborder(self, container):
        if type(container) == list:
            container.append(self)
        else:
            self.placeholder = container
        return container
        
    def resolve(self, indentation, tabreplacement, environment):
        self.regexp.resolve(indentation, tabreplacement, environment)    

#Snippet variables
class VariableTabstop(Node):
    def __init__(self, scope, parent = None):
        super(VariableTabstop, self).__init__(scope, parent)
        self.name = None
        self.value = ""

    def __deepcopy__(self, memo):
        node = VariableTabstop(self.scope, memo["parent"])
        node.name = self.name
        return node

    def __str__(self):
        return self.value

    def close(self, scope, text):
        node = self
        if scope == 'string.env.snippet':
            self.name = text
        else:
            return super(VariableTabstop, self).close(scope, text)
        return node
    
    def resolve(self, indentation, tabreplacement, environment):
        if self.name in environment:
            self.value = environment[self.name]

class VariablePlaceholder(Snippet):
    def __init__(self, scope, parent = None):
        super(VariablePlaceholder, self).__init__(scope, parent)
        self.name = None
        self.value = ""

    def __deepcopy__(self, memo):
        node = VariablePlaceholder(self.scope, memo["parent"])
        memo["parent"] = node
        for child in self:
            node.append(deepcopy(child, memo))
        node.name = self.name
        return node

    def __str__(self):
        return self.value or super(VariablePlaceholder, self).__str__()

    def close(self, scope, text):
        node = self
        if scope == 'string.env.snippet':
            self.name = text
        else:
            return super(VariablePlaceholder, self).close(scope, text)
        return node
    
    def resolve(self, indentation, tabreplacement, environment):
        if self.name in environment:
            self.value = environment[self.name]

class VariableTransformation(Node):
    def __init__(self, scope, parent = None):
        super(VariableTransformation, self).__init__(scope, parent)
        self.name = None
        self.value = ""
        self.regexp = None

    def __str__(self):
        return "".join(self.regexp.transform(self.value))

    def __deepcopy__(self, memo):
        node = VariableTransformation(self.scope, memo["parent"])
        memo["parent"] = node
        node.name = self.name
        node.regexp = deepcopy(self.regexp, memo)
        return node
        
    def open(self, scope, text):
        node = self
        if scope == 'string.regexp':
            node = self.regexp = Regexp(scope, self)
        else:
            return super(VariableTransformation, self).open(scope, text)
        return node
        
    def close(self, scope, text):
        node = self
        if scope == 'string.env.snippet':
            self.name = text
        else:
            return super(VariableTransformation, self).close(scope, text)
        return node
    
    def resolve(self, indentation, tabreplacement, environment):
        if self.name in environment:
            self.value = environment[self.name]
        self.regexp.resolve(indentation, tabreplacement, environment)

class Regexp(NodeList):
    _repl_re = onig_compile(r"\$(?:(\d+)|g<(.+?)>)")
    
    def __init__(self, scope, parent = None):
        super(Regexp, self).__init__(scope, parent)
        self.pattern = ""
        self.options = None

    def __deepcopy__(self, memo):
        node = Regexp(self.scope, memo["parent"])
        memo["parent"] = node
        for child in self:
            node.append(deepcopy(child, memo))
        node.pattern = self.pattern
        node.options = self.options
        return node

    def open(self, scope, text):
        node = self
        if scope == 'string.regexp.format':
            self.pattern += text[:-1]
            self.pattern = onig_compile(self.pattern)
        elif scope == 'meta.structure.condition.regexp':
            self.append(text.replace('\\n', '\n').replace('\\t', '\t'))
            node = Condition(scope, self)
            self.append(node)
        elif scope == 'constant.character.escape.regexp':
            #Escape in pattern
            if isinstance(self.pattern, (str, unicode)):
                self.pattern += text
            else:
                self.append(text.replace('\\n', '\n').replace('\\t', '\t'))
        else:
            return super(Regexp, self).open(scope, text)
        return node

    def close(self, scope, text):
        node = self
        if scope == 'string.regexp.format':
            self.append(text)
        elif scope == 'string.regexp.options':
            self.options = text
        elif scope == 'constant.character.escape.regexp':
            #Escape in pattern
            if isinstance(self.pattern, (str, unicode)):
                self.pattern += text
            else:
                self.append(text)
        else:
            return super(Regexp, self).close(scope, text)
        return node
    
    @staticmethod
    def uppercase(text):
        titles = text.split('\u')
        text = "".join([titles[0]] + map(lambda txt: txt[0].upper() + txt[1:], titles[1:]))
        uppers = text.split('\U')
        text = "".join([uppers[0]] + map(lambda txt: txt.find('\E') != -1 and txt[:txt.find('\E')].upper() + txt[txt.find('\E') + 2:] or txt.upper(), uppers ))
        return text

    @staticmethod
    def lowercase(text):
        lowers = text.split('\L')
        text = "".join([lowers[0]] + map(lambda txt: txt.find('\E') != -1 and txt[:txt.find('\E')].lower() + txt[txt.find('\E') + 2:] or txt.lower(), lowers ))
        return text
    
    @staticmethod
    def prepare_replacement(text):
        repl = None
        def expand(m, template):
            def handle(match):
                numeric, named = match.groups
                if numeric:
                    return m.group(int(numeric))
                return m.group(named)
            return Regexp._repl_re.sub(handle, template)
        if '$' in text:
            repl = lambda m, r = text: expand(m, r)
        else:
            repl = lambda m, r = text: r
        return repl

    def transform(self, text):
        result = ""
        for child in self:
            if isinstance(child, TextNode):
                repl = self.prepare_replacement(str(child))
                result += self.pattern.sub(repl, text)
            elif isinstance(child, Condition):
                for match in self.pattern.find(text):
                    if match[child.index] != None:
                        repl = child.insertion
                    else:
                        repl = child.otherwise
                    if repl == None:
                        break
                    repl = self.prepare_replacement(repl)
                    result += self.pattern.sub(repl, str(match))
                    if self.options == None or 'g' not in self.options:
                        break;
        if any(map(lambda r: result.find(r) != -1, ['\u', '\U'])):
            result = Regexp.uppercase(result)
        if any(map(lambda r: result.find(r) != -1, ['\L'])):
            result = Regexp.lowercase(result)
        return result
    
class Shell(NodeList):    
    def close(self, scope, text):
        node = self
        if scope == 'string.script':
            self.append(text)
        else:
            return super(Shell, self).close(scope, text)
        return node
    
    def resolve(self, indentation, tabreplacement, environment):
        descriptor, name = tempfile.mkstemp(prefix='pmx')
        file = os.fdopen(descriptor, 'w+')
        file.write(str(self).encode('utf8'))
        file.close()
        os.chmod(name, stat.S_IEXEC | stat.S_IREAD | stat.S_IWRITE)
        process = Popen([name], stdout=PIPE, stderr=STDOUT, env = environment, shell=True)
        self.clear()
        result = process.stdout.read()
        self.append(result.strip())
        process.stdout.close()

class Condition(Node):
    def __init__(self, scope, parent = None):
        super(Condition, self).__init__(scope, parent)
        self.index = None
        self.insertion = None
        self.otherwise = None
        self.current = ""
        
    def __deepcopy__(self, memo):
        node = Condition(self.scope, memo["parent"])
        node.index = self.index
        node.insertion = self.insertion
        node.otherwise = self.otherwise
        return node
    
    def open(self, scope, text):
        node = self
        if scope == 'otherwise.condition':
            self.current += text[:-1].replace('\\n', '\n').replace('\\t', '\t')
            self.insertion = self.current
            self.current = ""
        else:
            return super(Condition, self).open(scope, text)
        return node
    
    def close(self, scope, text):
        node = self
        if scope == 'string.regexp.condition':
            self.index = int(text)
        elif scope == 'text.condition' and self.insertion == None:
            self.current += text.replace('\\n', '\n').replace('\\t', '\t')
            self.insertion = self.current
        elif scope == 'keyword.escape.condition':
            self.current += text.replace('\\n', '\n').replace('\\t', '\t')
        elif scope == 'otherwise.condition':
            self.current += text.replace('\\n', '\n').replace('\\t', '\t')
            self.otherwise = self.current
            self.current = ""
        else:
            return super(Condition, self).close(scope, text)
        return node
    
    def append(self, element):
        self.current += element.replace('\\n', '\n').replace('\\t', '\t')
        
    def resolve(self, indentation, tabreplacement, environment):
        self.insertion = self.insertion.replace('\n', '\n' + indentation).replace('\t', tabreplacement)

class PMXSnippetProcessor(PMXSyntaxProcessor):
    def __init__(self):
        self.current = None
        self.node = Snippet("root")
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
        self.index = -1
        
    def __deepcopy__(self, memo):
        snippet = PMXSnippet(deepcopy(self.hash), deepcopy(self.name_space))
        memo["snippet"] = deepcopy(self.snippet, memo)
        snippet.bundle = self.bundle
        return snippet
    
    def __str__(self):
        return str(self.snippet)
    
    def __unicode__(self):
        return unicode(self.snippet)
    
    def __len__(self):
        return len(self.snippet)
    
    def setStarts(self, value):
        self.snippet.starts = value
        
    def getStarts(self):
        return self.snippet.starts
    
    starts = property(getStarts, setStarts)
    
    def setEnds(self, value):
        self.snippet.ends = value
        
    def getEnds(self):
        return self.snippet.ends
    
    ends = property(getEnds, setEnds) 
    
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
        if type(last) == list:
            last = last.pop()
        keys = taborder.keys()
        keys.sort()
        for key in keys:
            holder = taborder.pop(key)
            if type(holder) == list:
                if len(holder) == 1:
                    holder = holder.pop()
                else:
                    #Esto puede dar un error pero me interesa ver si hay casos asi
                    tabstop = filter(lambda node: isinstance(node, StructureTabstop), holder).pop()
                    transformations = filter(lambda node: isinstance(node, StructureTransformation), holder)
                    for transformation in transformations:
                        transformation.placeholder = tabstop
                    holder = tabstop
            self.taborder.append(holder)
        self.taborder.append(last)

    def getHolder(self, start, end = None):
        ''' Return the placeholder for position, where starts > position > ends'''
        end = end != None and end or start
        found = (0, None)
        for holder in self.taborder:
            # if holder == None then is the end of taborders
            if holder == None: break
            index = holder.position()
            if index <= start <= index + len(holder) and index <= end <= index + len(holder) and (found[1] == None or len(holder) < len(found[1])):
                found = (index, holder)
        if found[1] != None:
            setattr(found[1], 'last', found[1] == self.taborder[-1])
        return found
    
    def setCurrentHolder(self, holder):
        self.index = self.taborder.index(holder)
    
    def setDefaultHolder(self, start, end = None):
        (index, holder) = self.getHolder(start, end)
        if holder != None:
            self.setCurrentHolder(holder)
        return (index, holder)
    
    def current(self):
        if self.index == -1:
            self.index = 0
        return self.taborder[self.index]

    def next(self):
        if self.index < len(self.taborder) - 1:
            self.index += 1
        while self.taborder[self.index] != None and self.taborder[self.index] not in self.snippet:
            self.taborder.pop(self.index)
        return self.taborder[self.index]

    def previous(self):
        if self.index > 0:
            self.index -= 1
        while self.taborder[self.index] not in self.snippet:
            self.taborder.pop(self.index)
        return self.taborder[self.index]
    
    def resolve(self, indentation = "", tabreplacement = "\t", environment = {}):
        self.snippet.resolve(indentation, tabreplacement, environment)
    
    def write(self, index, text):
        if index < len(self.taborder) and self.taborder[index] != None and hasattr(self.taborder[index], "insert"):
            self.taborder[index].clear()
            self.taborder[index].insert(text, 0)