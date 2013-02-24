#!/usr/bin/env python
# -*- coding: utf-8 -*-

# VT100 Constants and masks

#modesoff SGR0         Turn off character attributes          ^[[m
#modesoff SGR0         Turn off character attributes          ^[[0m
SGR0 = 0x00000000

#bold SGR1             Turn bold mode on                      ^[[1m
SGR1 = 0x00010000
#lowint SGR2           Turn low intensity mode on             ^[[2m
#underline SGR4        Turn underline mode on                 ^[[4m
SGR4 = 0x00020000
#blink SGR5            Turn blinking mode on                  ^[[5m
#reverse SGR7          Turn reverse video on                  ^[[7m
SGR7 = 0x00040000
#invisible SGR8        Turn invisible text mode on            ^[[8m
SGR8 = 0x00080000

# Default foreground color
SGR39 = 0x10000000

# Default background color
SGR49 = 0x20000000

DEFAULTSGR = SGR39 | SGR49