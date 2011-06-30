#!/usr/bin/env ruby
FILENAME = ENV['TM_FILENAME']
FILEPATH = ENV['TM_FILEPATH']
SUPPORT  = ENV['TM_BUNDLE_SUPPORT']

BINARY   = "#{SUPPORT}/bin/jsl.exe"
REALFILE = %x{cygpath -ws "#{FILEPATH}"}.chomp
WIN32PATH = %x{cygpath -ws "#{SUPPORT}/conf/jsl.textmate.conf"}.chomp
output = `"#{BINARY}" -process "#{REALFILE}" -nologo -conf "#{WIN32PATH}"`

# the "X error(s), Y warning(s)" line will always be at the end
results = output.split(/\n/).pop
puts results unless results == "0 error(s), 0 warning(s)"
