###############################################################################
# JavaScript compatibility layer
###############################################################################

try:
        [].append(0)
        import re
        def match(pattern, text):
                m = re.match(pattern, text, re.MULTILINE)
                if m:
                        return m.group(0) == text
        def join(t):
                return '·'.join(t)
        def strip(t):
                return t.strip()
        def backslash(txt):
                return txt.replace('\n','\\n').replace('\t','\\t')
        context = "Python"
        body = None
except:
        o = Object
        o.defineProperty(Array.prototype, 'append' ,
                        {'enumerable': False,'value': Array.prototype.push})
        def match(pattern, text):
                return text.replace(RegExp(pattern), '') == ''
        def join(t):
                return t.join('·')
        def strip(t):
                return t.trim()
        def str(x):
                return '' + x
        def backslash(txt):
                return txt.replace(RegExp('\n','g'),'\\n'
                         ).replace(RegExp('\t','g'),'\\t')
        context = "JavaScript"
        try:
                body = document.getElementsByTagName('BODY')[0]
        except:
                body = None
