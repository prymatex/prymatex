#! /usr/bin/env ruby
require "bbcode.rb"

text = STDIN.read
print '<font face="Verdana" size="2">'
print text.bbcode_to_html
print '</font>'