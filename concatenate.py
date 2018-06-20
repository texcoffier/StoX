#!/usr/bin/python3

import sys
import json

functionalities = {}
s = []
for filename in sys.argv[1:]:
        s.append('if selected("{}"):\n'.format(filename[:-3]))
        doc = ""
        with open(filename, 'r') as f:
                state = 'first'
                for line in f:
                        if state == 'first' and line.startswith(("'''", '"""')):
                                state = 'in'
                                line = line[3:]
                        if state == 'in':
                                if line.strip().endswith(("'''", '"""')):
                                        state = 'out'
                                        line = line.strip()[:-3]
                                doc += line
                                continue
                        state = ''
                        s.append('    ' + line)
                functionalities[filename[:-3]] = doc

print('''
disabled_functionalities = []

def selected(name):
    try:
        import re
        if ('-' + name) in re.sys.argv:
            disabled_functionalities.append(name)
            return False
    except:
        if ('-' + name) in window.location.toString():
            disabled_functionalities.append(name)
            return False
    return True
functionalities = ''', json.dumps(functionalities), ';')
with open('required.py', 'r') as f:
        print(f.read())
print(''.join(s))
