# -*- coding: utf-8 -*-
#!/usr/bin/env python

import os
import re
import string

# Configuration for urlize() function.
TRAILING_PUNCTUATION = ['.', ',', ':', ';']
WRAPPING_PUNCTUATION = [('(', ')'), ('<', '>'), ('&lt;', '&gt;')]

# List of possible strings used for bullets in bulleted lists.
DOTS = ['&middot;', '*', '\u2022', '&#149;', '&bull;', '&#8226;']

unencoded_ampersands_re = re.compile(r'&(?!(\w+|#\d+);)')
unquoted_percents_re = re.compile(r'%(?![0-9A-Fa-f]{2})')
word_split_re = re.compile(r'(\s+)')
number_search_re = re.compile(r'(\d+)')
simple_url_re = re.compile(r'^https?://\w')
simple_abspath_re = re.compile(r'(/[\w\d\/\.-]+)')
simple_url_2_re = re.compile(r'^www\.|^(?!http)\w[^@]+\.(com|edu|gov|int|mil|net|org)$')
simple_email_re = re.compile(r'^\S+@\S+\.\S+$')
link_target_attribute_re = re.compile(r'(<a [^>]*?)target=[^\s>]+')
html_gunk_re = re.compile(r'(?:<br clear="all">|<i><\/i>|<b><\/b>|<em><\/em>|<strong><\/strong>|<\/?smallcaps>|<\/?uppercase>)', re.IGNORECASE)
hard_coded_bullets_re = re.compile(r'((?:<p>(?:%s).*?[a-zA-Z].*?</p>\s*)+)' % '|'.join([re.escape(x) for x in DOTS]), re.DOTALL)
trailing_empty_content_re = re.compile(r'(?:<p>(?:&nbsp;|\s|<br \/>)*?</p>\s*)+\Z')
file_abspath_line = re.compile(r'(?P<text>(?P<path>/[\w\d\/\.]+):|",[\s\w]+(?P<line>\d+))', re.VERBOSE)

def escape(html):
    return html.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#39;').replace("`", "&#145;")

def urlize(text, trim_url_limit = None, nofollow = False, autoescape = False):
    """
    Converts any URLs in text into clickable links.

    Works on http://, https://, www. links, and also on links ending in one of
    the original seven gTLDs (.com, .edu, .gov, .int, .mil, .net, and .org).
    Links can have trailing punctuation (periods, commas, close-parens) and
    leading punctuation (opening parens) and it'll still do the right thing.

    If trim_url_limit is not None, the URLs in link text longer than this limit
    will truncated to trim_url_limit-3 characters and appended with an elipsis.

    If nofollow is True, the URLs in link text will get a rel="nofollow"
    attribute.

    If autoescape is True, the link text and URLs will get autoescaped.
    """
    trim_url = lambda x, limit=trim_url_limit: limit is not None and (len(x) > limit and ('%s...' % x[:max(0, limit - 3)])) or x
    words = word_split_re.split(text)
    for i, word in enumerate(words):
        match = None
        if '.' in word or '@' in word or ':' in word or '/' in word:
            # Deal with punctuation.
            lead, middle, trail = '', word, ''
            for punctuation in TRAILING_PUNCTUATION:
                if middle.endswith(punctuation):
                    middle = middle[:-len(punctuation)]
                    trail = punctuation + trail
            for opening, closing in WRAPPING_PUNCTUATION:
                if middle.startswith(opening):
                    middle = middle[len(opening):]
                    lead = lead + opening
                # Keep parentheses at the end only if they're balanced.
                if (middle.endswith(closing)
                    and middle.count(closing) == middle.count(opening) + 1):
                    middle = middle[:-len(closing)]
                    trail = closing + trail

            # Make URL we want to point to.
            url = None
            nofollow_attr = ' rel="nofollow"' if nofollow else ''
            if simple_url_re.match(middle):
                url = middle
            elif simple_url_2_re.match(middle):
                url = 'http://%s' % middle
            elif not ':' in middle and simple_email_re.match(middle):
                local, domain = middle.rsplit('@', 1)
                domain = domain.encode('idna')
                url = 'mailto:%s@%s' % (local, domain)
                nofollow_attr = ''

            # Make link.
            if url:
                trimmed = trim_url(middle)
                if autoescape:
                    lead, trail = escape(lead), escape(trail)
                    url, trimmed = escape(url), escape(trimmed)
                middle = '<a href="%s"%s>%s</a>' % (url, nofollow_attr, trimmed)
                words[i] = '%s%s%s' % (lead, middle, trail)
            else:
                if autoescape:
                    words[i] = escape(word)
        elif autoescape:
            words[i] = escape(word)
    return ''.join(words)

def clean_html(text):
    """
    Clean the given HTML.  Specifically, do the following:
        * Convert <b> and <i> to <strong> and <em>.
        * Encode all ampersands correctly.
        * Remove all "target" attributes from <a> tags.
        * Remove extraneous HTML, such as presentational tags that open and
          immediately close and <br clear="all">.
        * Convert hard-coded bullets into HTML unordered lists.
        * Remove stuff like "<p>&nbsp;&nbsp;</p>", but only if it's at the
          bottom of the text.
    """
    text = re.sub(r'<(/?)\s*b\s*>', '<\\1strong>', text)
    text = re.sub(r'<(/?)\s*i\s*>', '<\\1em>', text)
    text = fix_ampersands(text)
    # Remove all target="" attributes from <a> tags.
    text = link_target_attribute_re.sub('\\1', text)
    # Trim stupid HTML such as <br clear="all">.
    text = html_gunk_re.sub('', text)
    # Convert hard-coded bullets into HTML unordered lists.
    def replace_p_tags(match):
        s = match.group().replace('</p>', '</li>')
        for d in DOTS:
            s = s.replace('<p>%s' % d, '<li>')
        return '<ul>\n%s\n</ul>' % s
    text = hard_coded_bullets_re.sub(replace_p_tags, text)
    # Remove stuff like "<p>&nbsp;&nbsp;</p>", but only if it's at the bottom
    # of the text.
    text = trailing_empty_content_re.sub('', text)
    return text
    
def htmlize(text, autoescape = True):
    paths = set()
    lines = []
    for l, line in enumerate(text.splitlines()):
        words = word_split_re.split(line)
        lead = trail = ""
        fileIndex = filePath = lineNumber = None
        for i, word in enumerate(words):
            match = simple_abspath_re.search(word)
            if match:
                lead, middle, trail = word[:match.start()], match.group(), word[match.end():]
                if os.path.isfile(middle):
                    filePath = middle
                    paths.add("%s/" % os.path.dirname(filePath))
                    fileIndex = i
            if filePath is not None:
                match = number_search_re.search(word)
                # Atento a los numeros
                if match:
                    lineNumber = match.group()
                    break
        if filePath:
            url = "txmt://open/?url=%s" % filePath
            if lineNumber is not None:
                url += "&line=%s" % lineNumber
            words[fileIndex] = (filePath, url, lead, trail)
        lines.append(words)
    commonprefix = len(os.path.commonprefix(paths))
    for l, line in enumerate(lines):
        for w, word in enumerate(line):
            if isinstance(word, tuple):
                filePath, url, lead, trail = word
                trimmed = filePath[commonprefix:]
                if autoescape:
                    lead, trail = escape(lead), escape(trail)
                    url, trimmed = escape(url), escape(trimmed)
                lines[l][w] = '%s<a href="%s">%s</a>%s' % (lead, url, trimmed, trail)
            elif autoescape:
                lines[l][w] = escape(word)
        lines[l] = "".join(line)
    return "\n".join(lines)

def makeHyperlinks(text):
    print(file_abspath_line.split(text))
    return re.sub(file_abspath_line, pathToLink, text)
    
if __name__ == '__main__':
    print(urlize("holaMunDSos /etc/pepe www.google.com 452 3jhds f as12315sdf"))
    text = """Traceback (most recent call last):
  File "/home/likewise-open/SUPTRIB/dvanhaaster/Workspace/prymatex/prymatex/gui/mainwindow.py", line 7, in <module>
    from prymatex.qt import QtCore, QtGui
ImportError: No module named prymatex.qt
    """
    print(htmlize(text))