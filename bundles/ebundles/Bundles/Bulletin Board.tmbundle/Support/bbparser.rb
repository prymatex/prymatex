#! /usr/bin/env ruby
require "#{ENV['TM_BUNDLE_SUPPORT']}/bbcode.rb"

text = STDIN.read
print text.bbcode_to_html