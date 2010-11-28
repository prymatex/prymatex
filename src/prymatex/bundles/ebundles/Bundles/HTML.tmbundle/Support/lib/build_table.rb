#!/usr/bin/env ruby

TABS = ENV['TM_TAB_SIZE'].to_i
rows = ENV['TM_TABSTOP_1'].to_i
cells = ENV['TM_TABSTOP_2'].to_i
row_class = ENV['TM_TABSTOP_3']

def tabs
  " " * TABS
end

def table_row(row_num, row_class)
  unless row_class == "and an alternating row class" || row_class.empty?
    if row_num % 2 == 0
      "#{tabs}<tr>"
    else
      "#{tabs}<tr class=\"#{row_class}\">"
    end
  else
      "#{tabs}<tr>"
  end
end

puts "<table>"
rows.times do |row|
  puts table_row(row, row_class)
  cells.times do |cell|
    print "#{tabs*2}" if cell == 0
    print "<td></td>"
  end
  puts "\n#{tabs}</tr>"
end
puts "</table>"