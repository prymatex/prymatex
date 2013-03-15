#!/usr/bin/env python
# encoding: utf-8

from parser import Parser
from prymatex.support.utils import compileRegexp, OPTION_CAPTURE_GROUP, OPTION_MULTILINE

class Format(object):
    _repl_re = compileRegexp(u"\$(?:(\d+)|g<(.+?)>)")
    def __init__(self, format):
        self.format = Parser.format(format)

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
            return lambda m, r = text: expand(m, r)
        else:
            return lambda m, r = text: r
    
    def apply(self, pattern, text):
        result = ""
        for child in self.format.composites:
            if isinstance(child, basestring):
                repl = self.prepare_replacement(unicode(child))
                result += pattern.sub(repl, text)
            elif isinstance(child, ConditionType):
                for match in pattern.finditer(text):
                    repl = child.index <= len(match.groups()) != None and child.insertion or child.otherwise
                    if repl != None:
                        repl = self.prepare_replacement(repl)
                        result += pattern.sub(repl, match.group(0))
                    if not self.option_global:
                        break
        if any(map(lambda r: result.find(r) != -1, ['\u', '\U'])):
            result = Regexp.uppercase(result)
        if any(map(lambda r: result.find(r) != -1, ['\L'])):
            result = Regexp.lowercase(result)
        return result

class Transformation(object):
    def __init__(self):
        self.pattern = None
        self.format = None
        self.options = None

    def setPattern(self, pattern):
        self.pattern = pattern
        
    def setFormat(self, format):
        self.format = Format(format)
        
    def setOptions(self, options):
        self.options = options
    
    def transform(self, text):
        flags = [OPTION_CAPTURE_GROUP]
        if self.option_multiline:
            flags.append(OPTION_MULTILINE)
        pattern = compileRegexp(unicode(self.pattern), flags)
        return self.format.apply(pattern, text)
        #return result.replace('\n', '\n' + processor.indentation).replace('\t', processor.tabreplacement)
    
    @property
    def option_global(self):
        return self.options != None and 'g' in self.options or False
    
    @property
    def option_multiline(self):
        return self.options != None and 'm' in self.options or False
        
if __name__ == '__main__':
    f = Format("(?1:$1:<em>$0<em>)")
    print f.format