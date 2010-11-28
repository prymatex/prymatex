#!/usr/bin/env ruby

require	'zlib'

require 'set'

MARK = [0xFFFC].pack("U").freeze
parts = STDIN.read.split(MARK)
src = parts.join

# find all function calls
src.gsub!(/(if|while|for|switch|sizeof|sizeofA)\s*\(/, '')
functions = src.scan(/(?:(?!->).(?!@|\.).|^\s*)\b([a-z]+)(?=\()/).flatten.to_set

# collect paths to all man files involved
paths = functions.collect do |func|
  %x{ man 2>/dev/null -WS2:3 #{func} }.scan /.+/
end.flatten.sort.uniq

# harvest includes from man files
includes = Set.new
paths.each do |path|
    Zlib::GzipReader.open(path) do |io|
    in_synopsis = false
    io.each_line do |line|
      if in_synopsis then
        case line
        when /^In (\S+)$/:                  includes << $1
        when /     #include <(\S+)>$/:      includes << $1
        when /^.SH /:                       break
        end
      elsif line =~ /^\.SH SYNOPSIS/
        in_synopsis = true
      end
    end
  end
end

# figure out what we already included
included = src.scan(/^\s*#\s*(?:include|import)\s+<(\S+)>/).flatten.to_set

new_includes = (includes - included).collect do |inc|
  "#include <#{inc}>\n"
end.join

parts[0].sub!(/\A (?:
  ^ \s* (?:
     \/\/ .*                            # line comments
   | \/\* (?m:.*?) \*\/                 # comment blocks
   | \# \s* (?:include|import) \s+ <.*  # system includes
   |                                    # blank lines
  ) \s* $ \n )*/x, '\0' + new_includes)

print parts.join('${0}')
