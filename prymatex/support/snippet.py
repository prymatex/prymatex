#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

"""Snippte's module"""
import uuid as uuidmodule

from prymatex.utils import six

from prymatex.support.regexp import Transformation
from prymatex.support.bundle import PMXBundleItem, PMXRunningContext
from prymatex.support.processor import PMXSyntaxProcessor
from prymatex.support.syntax import PMXSyntax

SNIPPET_PARSER = PMXSyntax(uuidmodule.uuid1())
SNIPPET_PARSER.load({ 
 'patterns': [{'captures': {'1': {'name': 'keyword.escape.snippet'}},
               'match': '\\\\(\\\\|\\$|`)',
               'name': 'constant.character.escape.snippet'},
              #Structures
              #TabStop
              {'captures': {'1': {'name': 'keyword.tabstop.snippet'},
                            '2': {'name': 'keyword.tabstop.snippet'}},
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
               'contentName': 'string.transformation',
               'end': '\\}',
               'name': 'structure.transformation.snippet'},
              #Menu
              {'begin': '\\$\\{(\\d+)\\|',
               'beginCaptures': {'1': {'name': 'keyword.menu.snippet'}},
               'contentName': 'string.options',
               'end': '\\|\\}',
               'name': 'structure.menu.snippet'},
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
               'contentName': 'string.transformation',
               'end': '\\}',
               'name': 'variable.transformation.snippet'},
               #Shell
              {'begin': '`',
               'end': '`',
               'contentName': 'string.script',
               'name': 'string.interpolated.shell.snippet'}],
 'repository': {'escaped_char': {'match': '\\\\[/\\\\\\}\\{]',
                                 'name': 'constant.character.escape.regexp'},
                'substitution': {'begin': '/',
                                 'contentName': 'string.regexp.format',
                                 'end': '/([mg]?)/?',
                                 'endCaptures': {'1': {'name': 'string.regexp.options'}},
                                 'patterns': [{'include': '#escaped_char'}]}},
})

#Snippet Node Bases
class Node(object):
    def __init__(self, scope, parent = None):
        self.scope = scope
        self.parent = parent
        self.disable = False

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
    
class NodeList(list):
    def __init__(self, scope, parent = None):
        super(NodeList, self).__init__()
        self.scope = scope
        self.parent = parent
        self.__disable = False

    @property
    def disable(self):
        return self.__disable
        
    @disable.setter
    def disable(self, value):
        self.__disable = value
        for child in self:
            child.disable = value
        
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
        elif scope == 'structure.menu.snippet':
            self.append(text)
            node = StructureMenu(scope, self)
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
        
    def __str__(self):
        return "".join([six.text_type(node) for node in self])
    
    __unicode__ = __str__

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
        if isinstance(element, six.string_types):
            element = TextNode(element, self)
        super(NodeList, self).append(element)

#Basic TextNode
class TextNode(Node):
    def __init__(self, text, parent = None):
        super(TextNode, self).__init__("string", parent)
        self.text = text.replace('\\n', '\n').replace('\\t', '\t')

    def __len__(self):
        return len(self.text)
    
    def __str__(self):
        return self.text
    
    __unicode__ = __str__
    
    def render(self, processor):
        processor.insertText(self.text)
    
#Snippet root
class Snippet(NodeList):
    def __init__(self, scope, snippetItem):
        super(Snippet, self).__init__(scope)
        self.snippetItem = snippetItem

    def render(self, processor):
        self.start = processor.caretPosition()
        super(Snippet, self).render(processor)
        self.end = processor.caretPosition()

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
        self.start = processor.caretPosition()
        if self.placeholder != None:
            self.placeholder.render(processor, mirror = True)
        else:
            if hasattr(self, 'content'):
                processor.insertText(self.content)
        self.end = processor.caretPosition()
    
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
            self.start = processor.caretPosition()
        if hasattr(self, 'content'):
            processor.insertText(self.content)
        elif self.placeholder != None:
            self.placeholder.render(processor)
        else:
            super(StructurePlaceholder, self).render(processor)
        if not mirror:
            self.end = processor.caretPosition()
    
    def taborder(self, container):
        if type(container) == list and container:
            for element in container:
                element.placeholder = self
        elif isinstance(container, StructurePlaceholder):
            self.placeholder = container
            return container
        return self

    def setContent(self, content):
        #Pongo un contenido y se corto el arbol
        self.content = content
        self.disable = True
        
class StructureTransformation(Node):
    def __init__(self, scope, parent = None):
        super(StructureTransformation, self).__init__(scope, parent)
        self.placeholder = None
        self.index = None
        self.text = ""
        self.transformation = None
    
    def close(self, scope, text):
        node = self
        if scope == 'keyword.transformation.snippet':
            self.index = int(text)
        elif scope == 'string.transformation':
            self.text += text
            self.transformation = Transformation(self.text)
        else:
            return super(StructureTransformation, self).close(scope, text)
        return node
    
    def render(self, processor):
        processor.startTransformation(self.transformation)
        if self.placeholder != None:
            self.placeholder.render(processor, mirror = True)
        processor.endTransformation(self.transformation)
    
    def taborder(self, container):
        if type(container) == list:
            container.append(self)
        else:
            self.placeholder = container
        return container

    def append(self, text):
        self.text += text
        
class StructureMenu(Node):
    def __init__(self, scope, parent = None):
        super(StructureMenu, self).__init__(scope, parent)
        self.index = None
        self.placeholder = None
        self.options = None
        self.optionIndex = 0
    
    def close(self, scope, text):
        node = self
        if scope == 'keyword.menu.snippet':
            self.index = int(text)
        elif scope == 'string.options':
            self.options = text.split(",")
        else:
            return super(StructureMenu, self).close(scope, text)
        return node
    
    def render(self, processor, mirror = False):
        self.start = processor.caretPosition()
        if self.placeholder != None:
            self.placeholder.render(processor, mirror = True)
        else:
            if hasattr(self, 'content'):
                processor.insertText(self.content)
            else:
                processor.insertText(self.options[self.optionIndex])
        self.end = processor.caretPosition()
    
    def reset(self):
        self.optionIndex = 0
        super(StructureMenu, self).reset()
    
    def taborder(self, container):
        if type(container) == list:
            container.append(self)
        else:
            self.placeholder = container
        return container
        
    def setContent(self, content):
        self.content = content

    def setOptionIndex(self, index):
        self.optionIndex = index

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
        environment = processor.environmentVariables()
        if self.name in environment:
            processor.insertText(environment[self.name])

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
        self.start = processor.caretPosition()
        environment = processor.environmentVariables()
        if self.name in environment:
            processor.insertText(environment[self.name])
        else:
            super(VariablePlaceholder, self).render(processor)
        self.end = processor.caretPosition()
    
class VariableTransformation(Node):
    def __init__(self, scope, parent = None):
        super(VariableTransformation, self).__init__(scope, parent)
        self.name = None
        self.transformationSource = ""

    def close(self, scope, text):
        node = self
        if scope == 'string.env.snippet':
            self.name = text
        elif scope == 'string.transformation':
            self.transformationSource += text
            self.transformation = Transformation(self.transformationSource)
        else:
            return super(VariableTransformation, self).close(scope, text)
        return node
    
    def render(self, processor):
        environment = processor.environmentVariables()
        if self.name in environment:
            text = self.transformation.transform(environment[self.name])
            processor.insertText(text)
    
    def append(self, transformationChunk):
        self.transformationSource += transformationChunk

class Shell(NodeList):    
    def close(self, scope, text):
        node = self
        if scope == 'string.script':
            self.append(text)
        else:
            return super(Shell, self).close(scope, text)
        return node
    
    @property
    def manager(self):
        if not hasattr(self, "_manager"):
            item = self
            while not isinstance(item, Snippet):
                item = item.parent
            self._manager = item.snippetItem.manager
        return self._manager
    
    def execute(self, processor):
        def afterExecute(context):
            self.content = context.outputValue.strip()
        with PMXRunningContext(self, six.text_type(self), processor.environmentVariables()) as context:
            context.asynchronous = False
            self.manager.runProcess(context, afterExecute)
        
    def render(self, processor):
        if not hasattr(self, 'content'):
            self.execute(processor)
        processor.insertText(self.content)

class PMXSnippetSyntaxProcessor(PMXSyntaxProcessor):
    def __init__(self, snippetItem):
        self.current = None
        self.node = Snippet("root", snippetItem)
        self.taborder = {}

    def openTag(self, name, start):
        token = self.current[self.index:start]
        self.node = self.node.open(name, token)
        self.index = start
        
    def closeTag(self, name, end):
        token = self.current[self.index:end]
        self.node = self.node.close(name, token)
        if hasattr(self.node, 'index') and six.callable(getattr(self.node, 'taborder', None)):
            container = self.taborder.setdefault(self.node.index, [])
            if (self.node != container and self.node not in container):
                self.taborder[self.node.index] = self.node.taborder(container)
        self.index = end

    def beginLine(self, line):
        if self.current != None:
            if self.index != len(self.current):
                self.node.append(self.current[self.index:len(self.current)])
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
    
    def __init__(self, uuid):
        PMXBundleItem.__init__(self, uuid)
        self.snippet = None                     #TODO: Poner un mejor nombre, este es el snippet compilado
    
    def load(self, dataHash):
        PMXBundleItem.load(self, dataHash)
        for key in PMXSnippet.KEYS:
            setattr(self, key, dataHash.get(key, None))
    
    @property
    def hash(self):
        dataHash = super(PMXSnippet, self).hash
        for key in PMXSnippet.KEYS:
            value = getattr(self, key)
            if value != None:
                dataHash[key] = value
        return dataHash
    
    def save(self, namespace):
        PMXBundleItem.save(self, namespace)
        self.snippet = None
    
    @property
    def ready(self):
        return self.snippet != None
    
    def compile(self):
        processor = PMXSnippetSyntaxProcessor(self)
        SNIPPET_PARSER.parse(self.content, processor)
        self.snippet = processor.node
        self.addTaborder(processor.taborder)

    def execute(self, processor):
        if not self.ready:
            self.compile()
        self.reset()
        processor.startSnippet(self)
        self.render(processor)
        holder = self.nextHolder()
        if holder != None:
            processor.selectHolder(holder)
        else:
            processor.endSnippet(self)
    
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
        self.snippet.disable = False
        self.snippet.reset()
    
    def render(self, processor):
        processor.startRender()
        self.snippet.render(processor)
        processor.endRender()
        
    def addTaborder(self, taborder):
        self.taborder = []
        lastHolder = taborder.pop(0, None)
        #TODO: ver si se puede sacar este "if pop" porque tendria que venir bien
        if type(lastHolder) == list:
            lastHolder = lastHolder.pop()
        keys = list(taborder.keys())
        keys.sort()
        for key in keys:
            holder = taborder.pop(key)
            if type(holder) == list:
                if len(holder) == 1:
                    holder = holder.pop()
                else:
                    #Esto puede dar un error pero me interesa ver si hay casos asi
                    tabstop = filter(lambda node: isinstance(node, StructureTabstop), holder).pop()
                    transformations = [node for node in holder if isinstance(node, StructureTransformation)]
                    for transformation in transformations:
                        transformation.placeholder = tabstop
                    holder = tabstop
            holder.last = False
            self.taborder.append(holder)
        if lastHolder is not None:
            lastHolder.last = True
        #elif self.taborder:
        #    self.taborder[-1].last = True
        self.taborder.append(lastHolder)
            

    def getHolder(self, start, end = None):
        ''' Return the placeholder for position, where starts > positiσn > ends'''
        end = end != None and end or start
        found = None
        for holder in self.taborder:
            # if holder == None then is the end of taborders
            if holder is None: break
            if holder.start <= start <= holder.end and holder.start <= end <= holder.end and (found == None or len(holder) < len(found)):
                found = holder
        return found
    
    def setCurrentHolder(self, holder):
        self.index = self.taborder.index(holder)
    
    def currentHolder(self):
        if self.index == -1:
            self.index = 0
        return self.taborder[self.index]

    def nextHolder(self):
        if self.index < len(self.taborder) - 1:
            self.index += 1
        #Fix disabled holders and None (last position in snippet)
        while self.index < len(self.taborder) - 1 and self.taborder[self.index] is not None and self.taborder[self.index].disable:
            self.index += 1
        return self.taborder[self.index]

    def previousHolder(self):
        if self.index > 0:
            self.index -= 1
        while self.index != 0 and self.taborder[self.index].disable:
            self.index -= 1
        return self.taborder[self.index]
    
    def writeInHolder(self, index, text):
        self.write(index, text)
    
    def write(self, index, text):
        if index < len(self.taborder) and self.taborder[index] is not None and hasattr(self.taborder[index], "insert"):
            self.taborder[index].clear()
            self.taborder[index].insert(text, 0)
    
    def __len__(self):
        return len(self.taborder)
