#!/usr/bin/python3


###############################################################################
# Utilities
###############################################################################



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
except:
        o = Object
        o.defineProperty(Array.prototype, 'append' ,
                        {'enumerable': False,'value': Array.prototype.push})
        def match(pattern, text):
                return text.replace(RegExp(pattern), '') == ''
        def join(t):
                return t.join('·')
        def str(x):
                return '' + x
        
###############################################################################
# Create framework
###############################################################################

fontsize = 16

class Item:
        def __init__(self, char='', x=0, y=0, previous_items=[], next_items=[]):
                self.next_items     = next_items
                self.previous_items = previous_items
                self.char           = char
                self.x              = x
                self.y              = y
                for i in previous_items:
                        i.next_items = [self]
        def short(self):
                return str(self.x) + '×' + str(self.y) + ':' + self.char
        def long(self):
                v = self.short()
                if len(self.next_items):
                        v += ',next=' + join([i.short() 
                                            for i in self.next_items])
                if len(self.previous_items):
                        v += ',previous=' + join([i.short() 
                                                for i in self.previous_items])
                return v
        def dump(self):
                print("\t\t{", self.long(), "}")
        def xy(self):
                return [4 + 0.8 * fontsize * self.x,
                        fontsize + 1.1 * fontsize * self.y]
        def wh(self):
                return [len(self.char) * 0.8 * fontsize, 1.1 * fontsize]

class Block:
        def __init__(self):
                self.items          = []
                self.t              = -1
                self.next_block     = None
                self.previous_block = None
                self.methods        = {}
                self.cursor         = 0
        def get_filter(self, method):
                if method in self.methods:
                        return self.methods[method]
                else:
                        return []
        def add_filter(self, method, function):
                if method not in self.methods:
                        self.methods[method] = []
                self.methods[method].append(function)
        def call(self, method, args=None):
                for function in self.get_filter(method):
                        function(self, args)
        def change_line(self, item, direction, after):
                line = item.y + direction
                if after and item.char == '\n':
                        line += 1
                        x = 0
                else:
                        x = item.x + after
                if line < 0:
                        return [item, 0]
                last = None
                for i in self.items:
                        if i.y == line:
                                last = i
                                if i.x >= x:
                                        return [i, 0]
                        elif i.y > line:
                                return [last, 0]
                if last:
                        return [last, 1]
                else:
                        if self.items[-1].char == '\n':
                                return [self.items[-1], 1]
                        return [item, after]

        # Standard hooks
        def set_time   (self, t):         self.call('set_time'   , t)
        def dump       (self, args=None): self.call('dump'       , args)
        def init       (self, args=None): self.call('init'       , args)
        def html_init  (self, args=None): self.call('html_init'  , args)
        def html_draw  (self, args=None): self.call('html_draw'  , args)
        def draw_cursor(self, args=None): self.call('draw_cursor', args)
class Blocks(Block):
        def __init__(self):
                self.blocks  = []
                self.methods = {}
        def append(self, block):
                self.blocks.append(block)
                block.blocks = self
                if len(self.blocks) > 1:
                        self.blocks[-2].next_block = block
                        block.previous_block = self.blocks[-2]
        def get(self, name):
                for block in self.blocks:
                        if block.name == name:
                                return block
        def key        (self, key):       self.call('key'        , key)

###############################################################################
# Create the blocks
###############################################################################

class SRC(Block):
        name = "SRC"
class LEX(Block):
        name = "LEX"
class YAC(Block):
        name = "YAC"

blocks = Blocks()
blocks.append(SRC())
blocks.append(LEX())
blocks.append(YAC())

def blocks_dump(blocks, dummy_arg):
        print('<dump>')
        for block in blocks.blocks:
                print('\t<', block.name, 't=', block.t, '>')
                block.dump(dummy_arg)
                print('\t</', block.name, '>')
        print('</dump>')
blocks.add_filter('dump', blocks_dump)

def blocks_init(blocks, dummy_arg):
        for block in blocks.blocks:
                block.init(dummy_arg)
blocks.add_filter('init', blocks_init)

def blocks_html_init(blocks, body):
        blocks.element = document.createElement('DIV')
        body.appendChild(blocks.element)
        for block in blocks.blocks:
                block.html_init()
blocks.add_filter('html_init', blocks_html_init)

def blocks_html_draw(blocks, body):
        for block in blocks.blocks:
                block.html_draw()
blocks.add_filter('html_draw', blocks_html_draw)


###############################################################################
# Define the SRC behavior
###############################################################################

def SRC_init(block, dummy_args):
        block.cursor_visible = 1
blocks.get('SRC').add_filter('init', SRC_init)

def SRC_dump(block, dummy_args):
        dump_item = block.get_filter('dumpitem')
        for item in block.items:
                item.dump()
                for function in dump_item:
                        function(item)
blocks.get('SRC').add_filter('dump', SRC_dump)

def SRC_analyse(block, text):
        block.items = []
        x = y = 0
        for char in text:
                block.items.append(Item(char, x, y))
                block.items[-1].index = len(block.items) - 1
                if char == '\n':
                        x = 0
                        y += 1
                else:
                        x += 1
def SRC_set(block, text):
        if not hasattr(block, 'history'):
                block.history = []
        if len(block.history) != block.t + 1:
                block.history = block.history[:block.t]
        block.history.append(text)
        SRC_analyse(block, text)
        block.t += 1
        block.next_block.set_time(0)
blocks.get('SRC').add_filter('set', SRC_set)

def SRC_set_time(block, t):
        block.t = t
        SRC_analyse(block, block.history[t])
        block.next_block.set_time(0)
blocks.get('SRC').add_filter('set_time', SRC_set_time)

def canvas_html_init(block, dummy):
        block.element = document.createElement('CANVAS')
        block.element.width = 200
        block.element.height = 400
        block.element.style.width  = str(block.element.width) + 'px'
        block.element.style.height = str(block.element.height) + 'px'
        block.blocks.element.appendChild(block.element)
blocks.get('SRC').add_filter('html_init', canvas_html_init)

def SRC_html_draw(block, dummy):
        c = block.element.getContext("2d")
        c.fillStyle = "#FFF"
        c.clearRect(0, 0, 10000, 10000)
        c.fillStyle = "#000"
        c.font = str(fontsize) + "px monospace"
        for item in block.items:
                x, y = item.xy()
                c.fillText(item.char, x, y)
        if block.cursor_visible:
                block.draw_cursor()
blocks.get('SRC').add_filter('html_draw', SRC_html_draw)

def SRC_draw_cursor(block, dummy):
        right = False
        if block.cursor == 0 or len(block.items) == 0:
                item = Item()
        elif block.cursor < len(block.items):
                item = block.items[block.cursor]
        else:
                item = block.items[-1]
                right = True
        x, y = item.xy()
        w, h = item.wh()
        if right:
                if item.char == '\n':
                        y += fontsize
                        x = Item().x + 3
                else:
                        x += w
        c = block.element.getContext("2d")
        c.fillStyle = "#000"
        c.strokeStyle = "#F00"
        c.lineWidth = 3
        c.fillRect(x - 3, y - h + 5, 3, fontsize)
blocks.get('SRC').add_filter('draw_cursor', SRC_draw_cursor)

def SRC_key(blocks, key):
        src = blocks.get('SRC')
        content = src.history[src.t]
        if key == 'ArrowRight':
                if src.cursor < len(content):
                        src.cursor += 1
        elif key == 'ArrowLeft':
                if src.cursor > 0:
                        src.cursor -= 1
        elif key == 'Home':
                y = src.items[min(src.cursor, len(src.items)-1)].y
                while src.cursor > 0 and src.items[src.cursor-1].y == y:
                        src.cursor -= 1
        elif key == 'End':
                y = src.items[min(src.cursor, len(src.items)-1)].y
                while src.cursor < len(src.items)-1 and src.items[src.cursor+1].y == y:
                        src.cursor += 1
                if src.cursor == len(src.items)-1 and src.items[-1].char != '\n':
                        src.cursor += 1
        elif key == 'ArrowUp' or key == 'ArrowDown':
                if src.cursor == len(content):
                        if content[-1] == '\n':
                                after = 0
                        else:
                                after = 1
                        item = src.items[-1]
                else:
                        after = 0
                        item = src.items[src.cursor]
                if key == 'ArrowUp':
                        direction = -1
                else:
                        direction = 1
                item, after = src.change_line(item, direction, after)
                src.cursor = item.index + after
        elif key == 'Backspace':
                if src.cursor != 0:
                        new_content = content[:src.cursor-1] + content[src.cursor:]
                        src.call('set', new_content)
                        src.cursor -= 1
        elif key == 'Delete':
                if src.cursor != len(content):
                        new_content = content[:src.cursor] + content[src.cursor+1:]
                        src.call('set', new_content)
        elif len(key) == 1 or key == 'Enter':
                if key == 'Enter':
                        key = '\n'
                new_content = content[:src.cursor] + key + content[src.cursor:]
                src.call('set', new_content)
                src.cursor += 1
        else:
                print('key=', key)
        src.cursor_visible = 1
blocks.add_filter('key', SRC_key)


###############################################################################
# Define the LEX behavior
###############################################################################

blocks.get('LEX').add_filter('html_init', canvas_html_init)

def LEX_dump(block, dummy_args):
        dump_item = block.get_filter('dumpitem')
        for item in block.items:
                item.dump()
                for function in dump_item:
                        function(item)

blocks.get('LEX').add_filter('dump', LEX_dump)

def LEX_init(block, dummy):
        block.lexem = []
blocks.get('LEX').add_filter('init', LEX_init)

class Lexem:
        def __init__(self, data):
                self.name       = data[0]
                self.regexp     = data[1]
                self.background = data[2]
        def long(self):
                return self.name + ':' + self.regexp

def LEX_add_lexem(block, lexem):
        block.lexem.append(Lexem(lexem))
blocks.get('LEX').add_filter('add_lexem', LEX_add_lexem)

def LEX_set_time(block, t):
        block.t = t
        items = block.previous_block.items
        block.items = []
        previous_items = []
        previous_possibles = []
        previous_current = ''
        current = ''
        i = 0
        # The loop go too far in order to output the last lexem
        while i <= len(items):
                if False:
                        print('i=', i,
                              'p_items=',
                               join([i.short() for i in previous_items]),
                              'p_possibles=',
                               join([i.long() for i in previous_possibles]),
                              'p_current=', previous_current
                              )
                possibles = []
                if i != len(items):
                        item = items[i]
                        current += item.char
                        for lexem in block.lexem:
                                if match(lexem.regexp, current):
                                        possibles.append(lexem)
                        item.possibles = possibles
                if len(possibles) == 0:
                        if len(previous_possibles) == 1:
                                block.items.append(Item(previous_current,
                                                        previous_items[0].x,
                                                        previous_items[0].y,
                                                        previous_items))
                                block.items[-1].lexem = previous_possibles[0]
                                current = ''
                                previous_items = []
                                previous_possibles = block.lexem
                                previous_current = ''
                        else:
                                break
                else:
                        i += 1
                        previous_items.append(item)
                        previous_possibles = possibles
                        previous_current = current
        block.next_block.set_time(0)
blocks.get('LEX').add_filter('set_time', LEX_set_time)

def LEX_html_draw(block, dummy):
        src = blocks.get('SRC')
        SRC_html_draw(block) # 'src.html_draw()' draws on SRC canvas
        c = block.element.getContext("2d")
        for item in block.items:
                if not item.lexem:
                        continue
                item.cursor = False
                for i in item.previous_items:
                        if i.index == src.cursor - 1:
                                item.cursor = True
                                break
                c.strokeStyle = item.lexem.background
                x, y = item.xy()
                w, h = item.wh()
                c.strokeRect(x, y - h + 5, w - 3, h - 3)
                if item.cursor:
                        c.fillStyle = item.lexem.background + '8'
                        c.fillRect(x, y - h + 5, w - 3, h - 3)
        if src.cursor:
                possibles = src.items[src.cursor-1].possibles
                if possibles:
                        last_line = src.items[-1].y + 3
                        c.fillStyle = '#000'
                        for y, lexem in enumerate(possibles):
                                c.fillText(lexem.long(),
                                           0, (y + last_line) * fontsize)
blocks.get('LEX').add_filter('html_draw', LEX_html_draw)

###############################################################################
# Define the YAC behavior
###############################################################################

blocks.get('YAC').add_filter('dump', LEX_dump)
blocks.get('YAC').add_filter('html_init', canvas_html_init)

def YAC_init(block, dummy):
        block.rules = {}
        block.disabled = {}
blocks.get('YAC').add_filter('init', YAC_init)

class Rule:
        def __init__(self, data):
                self.lexems = []
                for x in data:
                        if len(x) == 1:
                                x = [x[0], '1']
                        self.lexems.append(x)
        def long(self):
                return self.name + ':' + self.lexems

def YAC_update_rule(block, rule):
        if rule[0] not in block.rules:
                block.rules[rule[0]] = []
        block.rules[rule[0]].append(Rule(rule[1]))
blocks.get('YAC').add_filter('update_rule', YAC_update_rule)


def matching(block, items, position, rule_name):
        """Returns the Item"""
        if rule_name == items[position].lexem.name:
                item = Item(rule_name + ':' + items[position].char)
                item.remaining = position + 1
                item.previous_items = [items[position]]
                return item
        if rule_name not in block.rules:
                return
        
        if rule_name in block.disabled:
                return
        block.disabled[rule_name] = True
        try:
                for rule in block.rules[rule_name]:
                        i = position
                        ok = True
                        found = []
                        for name, repeat in rule.lexems:
                                while True:
                                        match = matching(block, items, i, name)
                                        if match:
                                                found.append(match)
                                                i = match.remaining
                                                if repeat != '*':
                                                        break
                                        else:
                                                if repeat != '*':
                                                        ok = False
                                                break
                        if ok:
                                match = Item(rule_name)
                                match.remaining = i
                                match.children = found
                                return match
        finally:
                del block.disabled[rule_name]

def YAC_set_time(block, t):
        block.t = t
        root = matching(block, block.previous_block.items, 0, 'Program')
        if root:
                block.items = []
                def walk(item, x, y):
                        item.x = x
                        item.y = y
                        block.items.append(item)
                        x += 1
                        y += 1
                        if item.children:
                                for child in item.children:
                                        y = walk(child, x, y)
                        return y
                walk(root, 0, 0)
                
        else:
                block.items = []
blocks.get('YAC').add_filter('set_time', YAC_set_time)

def YAC_html_draw(block, dummy):
        src = blocks.get('SRC')
        SRC_html_draw(block) # 'src.html_draw()' draws on SRC canvas
        c = block.element.getContext("2d")
        for item in block.items:
                if len(item.previous_items) == 1 and item.previous_items[0].cursor:
                        c.strokeStyle = item.previous_items[0].lexem.background
                        x, y = item.xy()
                        w, h = item.wh()
                        c.strokeRect(x, y - h + 5, w - 3, h - 3)
        
blocks.get('YAC').add_filter('html_draw', YAC_html_draw)

###############################################################################
# Test
###############################################################################

def test_change_line():
        src = blocks.get('SRC')
        src.call('set', 'a\nab\na\n\na')
        src.call('set', 'a\nab\na\n\na\n')
        src.call('set', 'a\nab\na\n\na\naa\na')
        for t in [0, 1, 2]:
                src.set_time(t)
                char = 0
                tests = [
                        [0,0, 2,0], [1,0, 3,0], [0,0, 5,0], [1,0, 6,0],
                        [1,0, 6,0], [2,0, 7,0], [3,0, 7,0], [5,0, 8,0]
                        ]
                if t == 0:
                        more = [[7,0, 8,0], [7,0, 8,1]]
                elif t == 1:
                        more = [[7,0, 9,1], [7,0, 9,1], [8,0, 9,1]]
                else:
                        more = [[7,0,10,0], [7,0,11,0], [8,0,13,0],
                                [9,0,13,1], [9,0,13,1], [10,0,13,0],[11,0,13,1]]
                for i in more:
                        tests.append(i)
                afte = 0
                for item_before, after_before, item_after, after_after in tests:
                        if afte:
                                bug
                        if char == len(src.items):
                                afte = 1
                                char -= 1
                        else:
                                afte = 0
                        for direction, i, a in [[-1, item_before, after_before],
                                                [ 1, item_after , after_after]]:
                                item, after = src.change_line(src.items[char],
                                                              direction, afte)
                                if item.index != i or after != a:
                                        print("t=", t,
                                              "char=", char,
                                              "direction=", direction,
                                              "after=", afte)
                                        print("expected_item=", i,
                                              "expected_after=", a)
                                        print("computed item=", item.index,
                                              "computed after=", after)
                                        zeraze
                        char += 1
        print('test_change_line OK')


blocks.init()
blocks.get('LEX').call('add_lexem', ['word'        , '[a-zA-Z]+'   , '#0FF'])
blocks.get('LEX').call('add_lexem', ['number'      , '[0-9]+'      , '#FF0'])
blocks.get('LEX').call('add_lexem', ['separator'   , '[ \n\t]'     , '#000'])
blocks.get('LEX').call('add_lexem', ['operator'    , '[-+/*]'      , '#F0F'])
blocks.get('LEX').call('add_lexem', ['affectation' , '[=]'         , '#F00'])
blocks.get('LEX').call('add_lexem', ['open'        , '[(]'         , '#00F'])
blocks.get('LEX').call('add_lexem', ['close'       , '[)]'         , '#00F'])

s = ['separator', '*']
for rule in [
        ['Program'   , [['Statement', '*']]],
        ['Statement' , [s, ['word'], s, ['affectation'], s, ['Expression']]],
        ['Expression', [['Expression'], s, ['operator'], s, ['Expression']]],
        ['Expression', [['open'], s, ['Expression'], s, ['close']]],
        ['Expression', [['word']]],
        ['Expression', [['number']]],
]:
        blocks.get('YAC').call('update_rule', rule)
test_change_line()

try:
        body = document.getElementsByTagName('BODY')[0]
except:
        body = None

if body:
        def keyevent(event):
                event = event or window.event
                blocks.key(event.key)
                blocks.html_draw()
        def drawevent():
                blocks.html_draw()
                src = blocks.get('SRC')
                src.cursor_visible = 1 - src.cursor_visible

        blocks.get('SRC').call('set', 'a=4\nb=a+5+1')
        blocks.html_init(body)
        setInterval(drawevent, 400)
        window.addEventListener('keypress', keyevent, False)
else:
        blocks.dump()
        
