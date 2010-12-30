#!/usr/bin/env ruby

require 'chronic'

d = Chronic.parse(STDIN.read, :guess => false)

if d.class == Time
  print d.strftime('%e-%b-%Y/%R')
elsif d.class == Chronic::Span
  # Get minimal way to show the range
  print d.begin.strftime('%e-%b-%Y');
  if d.begin.hour != 0 or d.begin.min != 0
    print d.begin.strftime('/%R');
  end
end