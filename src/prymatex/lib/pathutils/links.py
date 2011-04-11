'''
Some utilities for path parsing
http://manual.macromates.com/en/using_textmate_from_terminal.html
'''

import re

ABSPATH_LINENO_RE = re.compile('''
    (?P<text>(?P<path>/[\w\d\/\.]+)(:(?P<line>\d+))?)
''', re.VERBOSE)


def path_to_link(match):
    path = match.group('path')
    attrs = {}
    attrs['url'] = 'file://%s' % match.group('path')
    attrs['line'] = match.group('line')
    #attrs['column'] = match.group('column')
    
    final_attrs = '?%s' % '?'.join(['%s=%s' % (k, v) 
                                        for k, v in attrs.iteritems() if v ])
    text = match.group('text')
    
    data = dict(attrs= final_attrs, 
                text= text)
    link = '<a href="txmt://open/%(attrs)s">%(text)s</a>' % data 
    return link

def make_hyperlinks(text):
    '''
    Replaces every path occurence for a link
    '''
    return re.sub(ABSPATH_LINENO_RE, path_to_link, text)

def test():
    test_output = '''
    Python Run Script /tmp/pmxJ3I40j showAsHTML /home/defo/workspace/python/prymatex/src/prymatex/share/Support/lib/escape.rb:23:in `e_url': private method `gsub' called for nil:NilClass (NoMethodError)
        from (erb):20:in `header'
        from /home/defo/workspace/python/prymatex/src/prymatex/share/Support/lib/tm/htmloutput.rb:90:in `header'
        from /home/defo/workspace/python/prymatex/src/prymatex/share/Support/lib/tm/htmloutput.rb:67:in `show'
        from /home/defo/workspace/python/prymatex/src/prymatex/share/Support/lib/tm/executor.rb:110:in `run'
        from /tmp/pmxJ3I40j:13
    '''
    print make_hyperlinks(test_output)
    
        


if __name__ == '__main__':
    test()