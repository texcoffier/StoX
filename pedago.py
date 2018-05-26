#!/usr/bin/python3

class Item:
        def __init__(self, previous_item=(), next_item=(), char='', x=0, y=0):
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
                        return ()
        def add_filter(self, method, function):
                if method not in self.methods:
                        self.methods[method] = []
                self.methods[method].append(function)
        def call(self, method, args=()):
                for function in self.get_filter(method):
                        function(self, args)
        def name(self):
                return self.__class__.__name__
class Blocks(Block):
        def __init__(self):
                self.blocks = []
                self.methods       = {}
        def append(self, block):
                self.blocks.append(block)
                if len(self.blocks) > 1:
                        self.blocks[-2].next_block = block
                        blocks.previous_block = self.blocks[-2]
        def get(self, name):
                for block in self.blocks:
                        if block.name() == name:
                                return block

###############################################################################
# Create the blocks
###############################################################################

class SRC(Block):
        pass
class LEX(Block):
        pass

blocks = Blocks()
blocks.append(SRC())
blocks.append(LEX())

def blocks_dump(blocks, dummy_args):
        print('<dump>')
        for block in blocks.blocks:
                print('\t<', block.name(), 't=', block.t, '>')
                block.call('dump')
                print('\t</', block.name(), '>')
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
                block.items.append(Item(char=char, x=x, y=y))
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

blocks.get('SRC').add_filter('set', SRC_set)

def SRC_set_time(block, t):
        assert(t < len(block.history))
        block.t = t
        SRC_analyse(block, block.history[t])

blocks.get('SRC').add_filter('set_time', SRC_set_time)

###############################################################################
# Test
###############################################################################

blocks.get('SRC').call('set', '')
blocks.get('SRC').call('set', 'a=\n9')
blocks.call('dump')
blocks.get('SRC').call('set_time', 0)
blocks.call('dump')

