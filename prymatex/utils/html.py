# -*- coding: utf-8 -*-
#!/usr/bin/env python

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
simple_url_re = re.compile(r'^https?://\w')
simple_url_2_re = re.compile(r'^www\.|^(?!http)\w[^@]+\.(com|edu|gov|int|mil|net|org)$')
simple_email_re = re.compile(r'^\S+@\S+\.\S+$')
link_target_attribute_re = re.compile(r'(<a [^>]*?)target=[^\s>]+')
html_gunk_re = re.compile(r'(?:<br clear="all">|<i><\/i>|<b><\/b>|<em><\/em>|<strong><\/strong>|<\/?smallcaps>|<\/?uppercase>)', re.IGNORECASE)
hard_coded_bullets_re = re.compile(r'((?:<p>(?:%s).*?[a-zA-Z].*?</p>\s*)+)' % '|'.join([re.escape(x) for x in DOTS]), re.DOTALL)
trailing_empty_content_re = re.compile(r'(?:<p>(?:&nbsp;|\s|<br \/>)*?</p>\s*)+\Z')
del x # Temporary variable

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
        if '.' in word or '@' in word or ':' in word:
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
    
if __name__ == '__main__':
    print(urlize("holaMunDSos <a href='http://www.google.com'>http://www.google.com</a> 452 3jhds f as12315sdf"))
