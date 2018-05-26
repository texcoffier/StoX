#!/usr/bin/python3

###############################################################################
# Utilities
###############################################################################


###############################################################################
# JavaScript compatibility layer
###############################################################################

try:
        [].append(0)
except:
        o = Object
        o.defineProperty(Array.prototype, 'append' ,
                        {'enumerable': False,'value': Array.prototype.push})
        
###############################################################################
# Create framework
###############################################################################

class Item:
        def __init__(self, char='', x=0, y=0, previous_item=[], next_item=[]):
                self.next_item     = next_item
                self.previous_item = previous_item
                self.char          = char
                self.x             = x
                self.y             = y
        def dump(self):
                print("\t\t{", self.x, self.y, self.char, "}")
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
        def set_time(self, t):          self.call('set_time', t)
        def dump    (self, dummy=None): self.call('dump', dummy)
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

###############################################################################
# Define the SRC behavior
###############################################################################

def SRC_dump(src, dummy_args):
        dump_item = src.get_filter('dumpitem')
        for item in src.items:
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

def LEX_dump(lex, dummy_args):
        dump_item = lex.get_filter('dumpitem')
        for item in lex.items:
                item.dump()
                for function in dump_item:
                        function(item)

blocks.get('LEX').add_filter('dump', LEX_dump)

def LEX_set_time(block, t):
        block.t = t
        items = block.previous_block.items
        for item in items:
                pass
        print("lex set time")

blocks.get('LEX').add_filter('set_time', LEX_set_time)



###############################################################################
# Test
###############################################################################

blocks.get('SRC').call('set', '')
blocks.get('SRC').call('set', 'a=\n9')
blocks.dump()
blocks.get('SRC').set_time(0)
blocks.dump()

