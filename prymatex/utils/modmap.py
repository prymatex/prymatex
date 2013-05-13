#!/usr/bin/env python
from __future__ import unicode_literals

# Copyright (c) 2010 Pablo Seminario <pabluk@gmail.com>
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import re
import subprocess

#install xmodmap 
def cmd_keymap_table():
    try:
        return subprocess.Popen(
               ['xmodmap','-pk'], stdout=subprocess.PIPE).communicate()[0]
    except:
        return ""
def cmd_modifier_map():
    try:
        return subprocess.Popen(
               ['xmodmap','-pm'], stdout=subprocess.PIPE).communicate()[0]
    except:
        return ""

def get_keymap_table():
    keymap = {}

    keymap_table = cmd_keymap_table()

    re_line = re.compile(b'0x\w+')
    for line in keymap_table.splitlines()[1:]:
        if len(line) > 0:
            keycode = re.search(b'\s+(\d+).*', line)
            if keycode:
                new_keysyms = []
                keycode = int(keycode.group(1))
                keysyms = re_line.findall(line)
                # When you press only one key
                unicode_char = ''
                try:
                    unicode_char = chr(int(keysyms[0], 16))
                except:
                    unicode_char = ''
                if unicode_char == '\x00':
                    unicode_char = ''
                new_keysyms.append(unicode_char)

                # When you press a key plus Shift key
                unicode_char = ''
                try:
                    unicode_char = chr(int(keysyms[1], 16))
                except:
                    unicode_char = ''
                if unicode_char == '\x00':
                    unicode_char = ''
                new_keysyms.append(unicode_char)

                # When you press a key plus meta (dead keys)
                unicode_char = ''
                try:
                    unicode_char = chr(int(keysyms[4], 16))
                except:
                    unicode_char = ''
                if unicode_char == '\x00':
                    unicode_char = ''
                new_keysyms.append(unicode_char)

                # When you press a key plus meta plus Shift key
                unicode_char = ''
                try:
                    unicode_char = chr(int(keysyms[5], 16))
                except:
                    unicode_char = ''
                if unicode_char == '\x00':
                    unicode_char = ''
                new_keysyms.append(unicode_char)

                #keymap[keycode-8] = new_keysyms
                keymap[keycode] = new_keysyms

    return keymap

def get_modifier_map():
    modifiers = {}

    modifier_map = cmd_modifier_map()

    re_line = re.compile(b'(0x\w+)')
    for line in modifier_map.splitlines()[1:]:
        if len(line) > 0:
            mod_name = re.match(b'(\w+).*', line)
            if mod_name:
                mod_name = mod_name.group(1)
                keycodes = re_line.findall(line)
                # Convert key codes from hex to dec for use them
                # with the keymap table
                keycodes =[ int(kc, 16) for kc in keycodes]
                
                modifiers[mod_name] = keycodes

    return modifiers

if __name__ == '__main__':
    from pprint import pprint
    pprint(get_keymap_table())
    pprint(get_modifier_map())