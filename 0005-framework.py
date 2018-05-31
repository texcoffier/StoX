###############################################################################
# Create framework
###############################################################################

class Item:
        error = False
        color = "#000" # The text color
        def __init__(self, char='', x=0, y=0, previous_items=[], next_items=[]):
                self.next_items     = next_items
                self.previous_items = previous_items
                self.char           = char # The text displayed on screen
                self.rule           = char # The node name (class)
                self.value          = char # The node real value
                self.x              = x
                self.y              = y
                self.children       = []
                for i in previous_items:
                        i.next_items = [self]
        def clone(self):
                item = Item(self.value)
                item.previous_items = [self]
                item.rule           = self.rule
                item.color          = self.color
                item.rule           = self.rule
                item.value          = self.value
                return item
        def short(self):
                return (str(int(self.x)) + '×' + str(int(self.y)) + ':'
                        + self.value + '<' + self.rule + '>')
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
                return [4 + 0.7 * self.block.fontsize * self.x,
                        self.block.fontsize
                        + self.block.line_spacing * self.block.fontsize * self.y]
        def wh(self):
                return [len(self.char) * self.block.fontsize * 0.7,
                        self.block.fontsize]
        def fillRect(self):
                x, y = self.xy()
                w, h = self.wh()
                self.block.ctx.fillStyle = self.color + "6"
                self.block.ctx.fillRect(x - 1, y - h, w, h + 2)
                self.block.ctx.fillStyle = '#000'
                self.block.ctx.fillText(self.char, x, y)
        def fillText(self):
                x, y = self.xy()
                if self.error:
                        w, h = self.wh()
                        self.block.ctx.fillStyle = "#F88"
                        self.block.ctx.fillRect(x - 1, y - h, w, h + 2)
                self.block.ctx.fillStyle = self.color
                self.block.ctx.fillText(self.char, x, y)
        def lines_to_children(self):
                if len(self.children) == 0:
                        return
                x, y = self.xy()
                self.block.ctx.strokeStyle = "#000"
                fs = self.block.fontsize / 2
                for child in self.children:
                        x2, y2 = child.xy()
                        if y2 == y or y == 0:
                                continue
                        self.block.ctx.beginPath()
                        self.block.ctx.moveTo(x2 - 2*fs, y + 1)
                        self.block.ctx.lineTo(x2 - 2*fs, y2 - fs)
                        self.block.ctx.lineTo(x2 - 1, y2 - fs)
                        self.block.ctx.stroke()

class Block:
        next_block     = None
        previous_block = None
        cursor         = 0
        fontsize       = 12
        line_spacing   = 1.3
        def __init__(self):
                self.items          = []
                self.t              = -1
                self.methods        = {}
                self.empty          = Item()
                self.empty.block    = self
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
        
        def append(self, item):
                item.index = len(self.items)
                self.items.append(item)
                item.block = self
                self.call('append', item)
                return item

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
        def key(self, key): self.call('key', key)

