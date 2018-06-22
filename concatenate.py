#!/usr/bin/python3

import sys
import json

functionalities = {}
functionalities_hook_defined = {}
functionalities_hook_used = {}
s = []
for filename in sys.argv[1:]:
        name = filename[:-3]
        s.append('if selected("{}"):\n'.format(name))
        doc = ""
        with open(filename, 'r') as f:
                state = 'first'
                hook_defined = set()
                hook_used = set()
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
                        if ".add_filter('" in line:
                            hook_defined.add(line.split(".add_filter('")[1]
                                             .split("'")[0])
                        if ".call('" in line:
                            hook_used.add(line.split(".call('")[1]
                                          .split("'")[0])
                functionalities[name] = doc
                functionalities_hook_defined[name] = sorted(hook_defined)
                functionalities_hook_used[name] = sorted(hook_used)

print('''
disabled_functionalities = []

def selected(name):
    try:
        import re
        if ('-' + name) in re.sys.argv:
            disabled_functionalities.append(name)
            return False
    except:
        try:
            if ('-' + name) in window.location.toString():
                disabled_functionalities.append(name)
                return False
        except:
            pass # nodejs
    return True
functionalities = ''', json.dumps(functionalities))
print('functionalities_hook_defined = ',
      json.dumps(functionalities_hook_defined))
print('functionalities_hook_used = ',
      json.dumps(functionalities_hook_used))
try:
    with open('TMP/required.py', 'r') as f:
            print(f.read())
except:
    print('required = {}')
print(''.join(s))
