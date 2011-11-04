#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    Snippte's module
'''
import re, logging
import uuid as uuidmodule

#TODO: Ver de usar compileRegexp de prymatex.support.utils
try:
    from ponyguruma import sre
    from ponyguruma.constants import OPTION_CAPTURE_GROUP, OPTION_MULTILINE
except Exception, e:
    sre = re
    OPTION_CAPTURE_GROUP = re.MULTILINE
    OPTION_MULTILINE = re.MULTILINE

from prymatex.support.bundle import PMXBundleItem
from prymatex.support.processor import PMXSyntaxProcessor
from prymatex.support.syntax import PMXSyntax
from prymatex.support.utils import prepareShellScript
from subprocess import Popen, PIPE, STDOUT

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
                                 'match': '\\\\([/\\)])',
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

    def open(self, scope, text):
        return self

    def close(self, scope, text):
        if scope == self.scope:
            return self.parent
        return self
    
    def reset(self):
        attrs = ['start', 'end', 'content']
        for attr in attrs:
            if hasattr(self, attr):
                delattr(self, attr)
    
    def __len__(self):
        if hasattr(self, 'start') and hasattr(self, 'end'):
            return self.end - self.start
        return 0
    
    def render(self, processor):
        pass
    
class TextNode(Node):
    def __init__(self, text, parent = None):
        super(TextNode, self).__init__("string", parent)
        self.text = text.replace('\\n', '\n').replace('\\t', '\t')

    def __len__(self):
        return len(self.text)
    
    def __unicode__(self):
        return self.text
    
    def render(self, processor):
        processor.insertText(self.text.replace('\n', '\n' + processor.indentation).replace('\t', processor.tabreplacement))

class NodeList(list):
    def __init__(self, scope, parent = None):
        super(NodeList, self).__init__()
        self.parent = parent
        self.scope = scope

    def open(self, scope, text):
        node = self
        if scope == 'constant.character.escape.snippet':
            self.append(text)
        elif scope == 'structure.tabstop.snippet':
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
        return node

    def close(self, scope, text):
        if scope == self.scope:
            return self.parent
        elif scope == 'keyword.escape.snippet':
            self.append(text)
        else:
            self.append(text)
        return self
    
    def reset(self):
        for child in self:
            child.reset()
        attrs = ['start', 'end', 'content']
        for attr in attrs:
            if hasattr(self, attr):
                delattr(self, attr)
    
    def __len__(self):
        if hasattr(self, 'start') and hasattr(self, 'end'):
            return self.end - self.start
        return 0
        
    def __unicode__(self):
        return u"".join([unicode(node) for node in self])
    
    def render(self, processor):
        for child in self:
            child.render(processor)
    
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
    
#Snippet root
class Snippet(NodeList):
    def __init__(self, scope, parent = None):
        super(Snippet, self).__init__(scope, parent)
        
    def render(self, processor):
        self.start = processor.cursorPosition()
        super(Snippet, self).render(processor)
        self.end = processor.cursorPosition()

#Snippet structures
class StructureTabstop(Node):
    def __init__(self, scope, parent = None):
        super(StructureTabstop, self).__init__(scope, parent)
        self.placeholder = None
        self.index = None

    def close(self, scope, text):
        node = self
        if scope == 'keyword.tabstop.snippet':
            self.index = int(text)
        else:
            return super(StructureTabstop, self).close(scope, text)
        return node

    def render(self, processor, mirror = False):
        self.start = processor.cursorPosition()
        if self.placeholder != None:
            self.placeholder.render(processor, mirror = True)
        else:
            if hasattr(self, 'content'):
                processor.insertText(self.content)
        self.end = processor.cursorPosition()
    
    def taborder(self, container):
        if type(container) == list:
            container.append(self)
        else:
            self.placeholder = container
        return container
        
    def setContent(self, content):
        self.content = content
    
class StructurePlaceholder(NodeList):
    def __init__(self, scope, parent = None):
        super(StructurePlaceholder, self).__init__(scope, parent)
        self.index = None
        self.placeholder = None
        
    def close(self, scope, text):
        node = self
        if scope == 'keyword.placeholder.snippet':
            self.index = int(text)
        else:
            return super(StructurePlaceholder, self).close(scope, text)
        return node
        
    def render(self, processor, mirror = False):
        if not mirror:
            self.start = processor.cursorPosition()
        if hasattr(self, 'content'):
            processor.insertText(self.content)
        elif self.placeholder != None:
            self.placeholder.render(processor)
        else:
            super(StructurePlaceholder, self).render(processor)
        if not mirror:
            self.end = processor.cursorPosition()
    
    def taborder(self, container):
        if type(container) == list and container:
            for element in container:
                element.placeholder = self
        elif isinstance(container, StructurePlaceholder):
            self.placeholder = container
            return container
        return self

    def setContent(self, content):
        self.content = content
        
class StructureTransformation(Node):
    def __init__(self, scope, parent = None):
        super(StructureTransformation, self).__init__(scope, parent)
        self.placeholder = None
        self.index = None
        self.regexp = None
    
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
    
    def render(self, processor):
        processor.startTransformation(self.regexp)
        if self.placeholder != None:
            self.placeholder.render(processor, mirror = True)
        processor.endTransformation(self.regexp)
    
    def taborder(self, container):
        if type(container) == list:
            container.append(self)
        else:
            self.placeholder = container
        return container

#Snippet variables
class VariableTabstop(Node):
    def __init__(self, scope, parent = None):
        super(VariableTabstop, self).__init__(scope, parent)
        self.name = None

    def close(self, scope, text):
        node = self
        if scope == 'string.env.snippet':
            self.name = text
        else:
            return super(VariableTabstop, self).close(scope, text)
        return node
    
    def render(self, processor):
        if self.name in processor.environment:
            processor.insertText(processor.environment[self.name])

class VariablePlaceholder(NodeList):
    def __init__(self, scope, parent = None):
        super(VariablePlaceholder, self).__init__(scope, parent)
        self.name = None

    def close(self, scope, text):
        node = self
        if scope == 'string.env.snippet':
            self.name = text
        else:
            return super(VariablePlaceholder, self).close(scope, text)
        return node
    
    def render(self, processor):
        self.start = processor.cursorPosition()
        if self.name in processor.environment:
            processor.insertText(processor.environment[self.name])
        else:
            super(VariablePlaceholder, self).render(processor)
        self.end = processor.cursorPosition()
    
class VariableTransformation(Node):
    def __init__(self, scope, parent = None):
        super(VariableTransformation, self).__init__(scope, parent)
        self.name = None
        self.regexp = None

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
    
    def render(self, processor):
        if self.name in processor.environment:
            text = self.regexp.transform(processor.environment[self.name], processor)
            processor.insertText(text)

class Regexp(NodeList):
    _repl_re = sre.compile(u"\$(?:(\d+)|g<(.+?)>)")
    
    def __init__(self, scope, parent = None):
        super(Regexp, self).__init__(scope, parent)
        self.pattern = ""
        self.options = None

    def open(self, scope, text):
        node = self
        if scope == 'string.regexp.format':
            self.pattern += text[:-1]
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
        if len(titles) > 1:
            text = "".join([titles[0]] + map(lambda txt: txt[0].upper() + txt[1:], titles[1:]))
        uppers = text.split('\U')
        if len(uppers) > 1:
            text = "".join([uppers[0]] + map(lambda txt: txt.find('\E') != -1 and txt[:txt.find('\E')].upper() + txt[txt.find('\E') + 2:] or txt.upper(), uppers ))
        return text

    @staticmethod
    def lowercase(text):
        lowers = text.split('\L')
        if len(lowers) > 1:
            text = "".join([lowers[0]] + map(lambda txt: txt.find('\E') != -1 and txt[:txt.find('\E')].lower() + txt[txt.find('\E') + 2:] or txt.lower(), lowers ))
        return text
    
    @staticmethod
    def prepare_replacement(text):
        repl = None
        def expand(m, template):
            def handle(match):
                numeric, named = match.groups()
                if numeric:
                    return m.group(int(numeric)) or ""
                return m.group(named) or ""
            return Regexp._repl_re.sub(handle, template)
        if '$' in text:
            repl = lambda m, r = text: expand(m, r)
        else:
            repl = lambda m, r = text: r
        return repl

    def transform(self, text, processor):
        flags = [OPTION_CAPTURE_GROUP]
        if self.option_multiline:
            flags.append(OPTION_MULTILINE)
        self.pattern = sre.compile(unicode(self.pattern), reduce(lambda x, y: x | y, flags, 0))
        result = ""
        for child in self:
            if isinstance(child, TextNode):
                repl = self.prepare_replacement(unicode(child))
                result += self.pattern.sub(repl, text)
            elif isinstance(child, Condition):
                for match in self.pattern.finditer(text):
                    repl = match.group(child.index) != None and child.insertion or child.otherwise
                    if repl != None:
                        repl = self.prepare_replacement(repl)
                        result += self.pattern.sub(repl, str(match))
                    if not self.option_global:
                        break
        if any(map(lambda r: result.find(r) != -1, ['\u', '\U'])):
            result = Regexp.uppercase(result)
        if any(map(lambda r: result.find(r) != -1, ['\L'])):
            result = Regexp.lowercase(result)
        return result.replace('\n', '\n' + processor.indentation).replace('\t', processor.tabreplacement)
    
    @property
    def option_global(self):
        return self.options != None and 'g' in self.options or False
    
    @property
    def option_multiline(self):
        return self.options != None and 'm' in self.options or False
    
class Shell(NodeList):    
    def close(self, scope, text):
        node = self
        if scope == 'string.script':
            self.append(text)
        else:
            return super(Shell, self).close(scope, text)
        return node
    
    def execute(self, processor):
        command, env = prepareShellScript(unicode(self), processor.environment)
        
        process = Popen(command, stdout=PIPE, stderr=STDOUT, env = env)
        text = process.stdout.read()
        text = text.strip()
        process.stdout.close()
        _ = process.wait()
        self.content = text.replace('\n', '\n' + processor.indentation).replace('\t', processor.tabreplacement)
        
    def render(self, processor):
        if not hasattr(self, 'content'):
            self.execute(processor)
        processor.insertText(self.content)

class Condition(Node):
    def __init__(self, scope, parent = None):
        super(Condition, self).__init__(scope, parent)
        self.index = None
        self.insertion = None
        self.otherwise = None
        self.current = ""
        
    def open(self, scope, text):
        node = self
        if scope == 'otherwise.condition':
            self.current += text[:-1].replace('\\n', '\n').replace('\\t', '\t')
            self.insertion = self.current
            self.current = ""
        elif scope == 'constant.character.escape.condition':
            self.current += text.replace('\\n', '\n').replace('\\t', '\t')
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

class PMXSnippetSyntaxProcessor(PMXSyntaxProcessor):
    def __init__(self):
        self.current = None
        self.node = Snippet("root")
        self.taborder = {}

    def openTag(self, name, start):
        token = self.current[self.index:start]
        self.node = self.node.open(name, token)
        self.index = start
        
    def closeTag(self, name, end):
        token = self.current[self.index:end]
        self.node = self.node.close(name, token)
        if hasattr(self.node, 'index') and callable(getattr(self.node, 'taborder', None)):
            container = self.taborder.setdefault(self.node.index, [])
            if (self.node != container and self.node not in container):
                self.taborder[self.node.index] = self.node.taborder(container)
        self.index = end

    def beginLine(self, line, stack):
        if self.current != None:
            if self.index != len(self.current):
                self.node.append(self.current[self.index:len(self.current)])
            self.node.append("\n")
        self.current = line
        self.index = 0
        
    def startParsing(self, name):
        self.node.open(name, "")

    def endParsing(self, name):
        token = self.current[self.index:len(self.current)]
        self.node.close(name, token)

class PMXSnippet(PMXBundleItem):
    KEYS = [ 'content', 'disableAutoIndent', 'inputPattern' ]
    TYPE = 'snippet'
    FOLDER = 'Snippets'
    EXTENSION = 'tmSnippet'
    PATTERNS = ['*.tmSnippet', '*.plist']
    parser = PMXSyntax(uuidmodule.uuid1(), "internal", hash = SNIPPET_SYNTAX)
    
    def __init__(self, uuid, namespace, hash, path = None):
        super(PMXSnippet, self).__init__(uuid, namespace, hash, path)
        self.snippet = None
    
    def load(self, hash):
        super(PMXSnippet, self).load(hash)
        for key in PMXSnippet.KEYS:
            setattr(self, key, hash.get(key, None))
    
    @property
    def hash(self):
        hash = super(PMXSnippet, self).hash
        for key in PMXSnippet.KEYS:
            value = getattr(self, key)
            if value != None:
                hash[key] = value
        return hash
    
    #override save for deprecate compiled snippet
    def save(self):
        super(PMXSnippet, self).save()
        self.snippet = None
    
    @property
    def ready(self):
        return self.snippet != None
    
    def compile(self):
        processor = PMXSnippetSyntaxProcessor()
        self.parser.parse(self.content, processor)
        self.snippet = processor.node
        self.addTaborder(processor.taborder)

    def execute(self, processor):
        if not self.ready:
            self.compile()
        self.reset()
        processor.startSnippet(self)
        self.render(processor)
        holder = self.next()
        if holder != None:
            processor.selectHolder(holder)
        else:
            processor.endSnippet()
    
    @property
    def start(self):
        if hasattr(self, 'snippet') and hasattr(self.snippet, 'start'):
            return self.snippet.start
        return 0
    
    @property    
    def end(self):
        if hasattr(self, 'snippet') and hasattr(self.snippet, 'end'):
            return self.snippet.end
        return 0
    
    def reset(self):
        self.index = -1
        self.snippet.reset()
    
    def render(self, processor):
        self.snippet.render(processor)
        
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
        found = None
        for holder in self.taborder:
            # if holder == None then is the end of taborders
            if holder == None: break
            if holder.start <= start <= holder.end and holder.start <= end <= holder.end and (found == None or len(holder) < len(found)):
                found = holder
        if found != None:
            setattr(found, 'last', found == self.taborder[-1])
        return found
    
    def setCurrentHolder(self, holder):
        self.index = self.taborder.index(holder)
    
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
    
    def write(self, index, text):
        if index < len(self.taborder) and self.taborder[index] != None and hasattr(self.taborder[index], "insert"):
            self.taborder[index].clear()
            self.taborder[index].insert(text, 0)