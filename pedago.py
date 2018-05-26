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
class Block:
        def __init__(self):
                self.items          = []
                self.t              = 0
                self.next_block     = None
                self.previous_block = None
                self.methods        = {}
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
        # Standard hooks
        def set_time(self, t):         self.call('set_time', t)
        def dump    (self, args=None): self.call('dump', args)
        def init    (self, args=None): self.call('init', args)
class Blocks(Block):
        def __init__(self):
                self.blocks  = []
                self.methods = {}
        def append(self, block):
                self.blocks.append(block)
                if len(self.blocks) > 1:
                        self.blocks[-2].next_block = block
                        block.previous_block = self.blocks[-2]
        def get(self, name):
                for block in self.blocks:
                        if block.name == name:
                                return block

###############################################################################
# Create the blocks
###############################################################################

class SRC(Block):
        name = "SRC"
class LEX(Block):
        name = "LEX"

blocks = Blocks()
blocks.append(SRC())
blocks.append(LEX())

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


###############################################################################
# Define the SRC behavior
###############################################################################

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
                if char == '\n':
                        x = 0
                        y += 1
                else:
                        x += 1
def SRC_set(block, text):
        if not hasattr(block, 'history'):
                block.history = []
        if len(block.history) != block.t:
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

###############################################################################
# Define the LEX behavior
###############################################################################

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
                self.name = data[0]
                self.regexp = data[1]
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
                if len(possibles) == 0:
                        if len(previous_possibles) == 1:
                                block.items.append(Item(previous_current,
                                                        previous_items[0].x,
                                                        previous_items[0].y,
                                                        previous_items))
                                block.items[-1].lexem = previous_possibles[0]
                                current = ''
                                previous_items = []
                                previous_possibles = []
                                previous_current = ''
                        else:
                                break
                else:
                        i += 1
                        previous_items.append(item)
                        previous_possibles = possibles
                        previous_current = current
        
                        
blocks.get('LEX').add_filter('set_time', LEX_set_time)



###############################################################################
# Test
###############################################################################

blocks.init()
blocks.get('LEX').call('add_lexem', ['word', '[a-z]+'])
blocks.get('LEX').call('add_lexem', ['number', '[-+]?[0-9]+'])
blocks.get('LEX').call('add_lexem', ['separator', '[ \n\t]'])
blocks.get('LEX').call('add_lexem', ['operator', '[=]'])
blocks.get('SRC').call('set', '')
blocks.get('SRC').call('set', 'ab=\n2018')
blocks.dump()
blocks.get('SRC').set_time(0)
blocks.dump()

