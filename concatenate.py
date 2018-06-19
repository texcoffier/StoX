#!/usr/bin/python3

import sys
import json

functionalities = {}
s = []
for filename in sys.argv[1:]:
        s.append('if selected("{}"):\n'.format(filename))
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
def selected(name):
    return True
functionalities = ''', json.dumps(functionalities), ';')
print(''.join(s))
