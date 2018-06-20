"""Core: heart of the framework: «Item», «Block» and «Blocks»"""

class Item:
        error = False
        color = "#000" # The text color
        arrow_to = None
        char_width = 0.7
        def __init__(self, char='', x=0, y=0, previous_items=None):
                if previous_items is None:
                        previous_items = []
                self.previous_items = previous_items
                self.char           = char # The text displayed on screen
                self.rule           = char # The node name (class)
                self.value          = char # The node real value
                self.x              = x
                self.y              = y
                self.children       = []
                self.next_items     = []
        def clone(self):
                item = Item(self.value)
                item.previous_items = [self]
                item.color          = self.color
                item.char           = self.char
                item.rule           = self.rule
                item.value          = self.value
                self.next_items     = []
                return item
        def set_byte(self, i):
                self.char = hex(i>>4) + hex(i)
                if not ( -128 <= i <= 127 ):
                        self.error = True
                        for item in self.previous_items:
                                item.error = True
                self.unsigned_value = i & 0xFF
                self.value = clamp(i)
                return self
        def set_word(self, i):
                self.value = i & 0xFFFF
                self.char = hex4(i)
                return self
        def short(self):
                return (str(int(self.x)) + '×' + str(int(self.y)) + ':'
                        + self.char + '<' + str(self.rule) + '>')
        def long(self):
                v = self.short()
                if len(self.previous_items):
                        v += ',previous=' + join([i.short() 
                                                for i in self.previous_items])
                return v
        def dump(self):
                print("\t\t{", self.long(), "}")
        def xy(self):
                return [4 + self.char_width * self.block.fontsize * self.x,
                        self.block.fontsize
                        + self.block.line_spacing * self.block.fontsize * self.y]
        def wh(self):
                return [len(self.char) * self.block.fontsize * self.char_width,
                        self.block.fontsize]
        def clipped(self):
                x, y = self.xy()
                w, h = self.wh()
                return x + w > self.block.element.parentNode.offsetWidth
        def fillRect(self):
                x, y = self.xy()
                w, h = self.wh()
                self.block.ctx.fillStyle = self.color + "6"
                if self.block.fullline_highlight:
                        self.block.ctx.fillRect(0, y - h, w + x, h + 2)
                else:
                        self.block.ctx.fillRect(x - 1, y - h, w, h + 2)
                self.block.ctx.fillStyle = '#000'
                self.block.ctx.fillText(self.char, x, y)
        def rectangle(self, color="#0008"):
                x, y = self.xy()
                w, h = self.wh()
                self.block.ctx.strokeStyle = color
                self.block.ctx.strokeRect(x - 1, y - h, w, h + 2)
        def contains(self, px, py):
                x, y = self.xy()
                w, h = self.wh()
                return x < px < x + w and y - h < py < y
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
        def draw_arrow(self):
                fs = self.block.fontsize
                tx = fs * (self.nr_arrows + 1) / 3
                x, y = self.xy()
                x += 1.7 * fs
                x2, y2 = self.block.items[self.arrow_to].xy()
                y2 -= fs / 3
                self.block.ctx.beginPath()
                self.block.ctx.moveTo(x + fs  , y - fs/2)
                self.block.ctx.lineTo(x - tx  , y - fs/2)
                self.block.ctx.lineTo(x - tx  , y2)
                self.block.ctx.lineTo(x       , y2)
                self.block.ctx.lineTo(x - fs/3, y2 - fs/3)
                self.block.ctx.lineTo(x - fs/3, y2 + fs / 3)
                self.block.ctx.lineTo(x       , y2)
                self.block.ctx.stroke()

class Block:
        next_block     = None
        previous_block = None
        cursor         = 0
        fontsize       = 8
        line_spacing   = 1.3
        time_travel    = False
        initialized    = False
        window_top     = True
        height         = 100 # Full window height
        fullline_highlight = False
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
        def add_filter(self, method, function, before=False):
                if method not in self.methods:
                        self.methods[method] = []
                if before:
                        self.methods[method].insert(0, function)
                else:
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
        def set_to_minimal_height(self):
                if not body:
                        return
                y = self.items[-1].y + 1
                height = y * block.line_spacing * block.fontsize
                block.element.height = height
                block.element.style.height = height + "px"

        # Standard hooks
        def dump       (self, args=None): self.call('dump'       , args)
        def init       (self, args=None):
                if not self.initialized:
                        self.call('init'       , args)
                        self.initialized = True
        def html_init  (self, args=None): self.call('html_init'  , args)
        def html_draw  (self, args=None): self.call('html_draw'  , args)
        def draw_cursor(self, args=None): self.call('draw_cursor', args)
        def set_time   (self, t):         self.call('set_time'   , t)
        
        def append(self, item, dy=None):
                if len(self.items) and dy is not None:
                        item.y = self.items[-1].y + dy
                item.index = len(self.items)
                self.items.append(item)
                item.block = self
                self.call('append', item)
                return item

class Blocks(Block):
        name = "blocks"
        def __init__(self):
                self.blocks  = []
                self.methods = {}
        def append(self, block):
                self.blocks.append(block)
                block.blocks = self
                if len(self.blocks) > 1:
                        self.blocks[-2].next_block = block
                        block.previous_block = self.blocks[-2]
                return block
        def key(self, key):
                self.call('key', key)
        def keyup(self, key):
                self.call('keyup', key)

def canvas_html_init(block, title):
        div = document.createElement('DIV')
        div.innerHTML = ('<div class="header">'
                         + '<div class="buttons"></div>'
                         + '<div class="title">' + title + '</div>'
                         + '</div>'
                         + '<canvas tabindex="0"></canvas>')
        div.style.display = "inline-block"
        div.style.verticalAlign = 'top'
        if block.window_top:
                block.blocks.element.appendChild(div)
        else:
                block.previous_block.element.parentNode.appendChild(div)
        block.buttons = div.firstChild.firstChild
        if block.time_travel:
                block.buttons.innerHTML = (
                          '<div class="time_travel">'
                        + '<button>◀ ' + block.time_travel[0] + '</button>'
                        + '<span></span>'
                        + '<button>' + block.time_travel[1] + ' ▶</button>'
                        + '</div>'
                        )
                tt = block.buttons.firstChild
                block.time_travel_t = tt.childNodes[1]
                def time_travel_back():
                        block.set_time(block.t - 1)
                def time_travel_forward():
                        block.set_time(block.t + 1)
                block.time_travel_back = time_travel_back
                block.time_travel_forward = time_travel_forward
                tt.childNodes[0].onclick = time_travel_back
                tt.childNodes[2].onclick = time_travel_forward
        block.element = div.childNodes[1]
        block.element.style.display = 'block'
        block.element.width = (4 * window_width) / blocks.nr_columns
        height = (block.height * window_height) / 100
        block.element.height = height - div.childNodes[0].offsetHeight
        block.element.style.width = str(block.element.width) + 'px'
        block.element.style.height = str(block.element.height) + 'px'
        block.ctx = block.element.getContext("2d")
        div.style.overflow = 'hidden'
        if block.window_top:
                div.style.width = str(window_width / blocks.nr_columns) + 'px'
        else:
                div.style.width = '100%'

        for b in blocks.blocks:
                b.add_filter('set_time', block_set_time)

def SRC_html_draw(block, dummy):
        block.ctx.fillStyle = "#FFF"
        block.ctx.clearRect(0, 0, 10000, 10000)
        block.ctx.font = str(block.fontsize) + "px monospace"

        for item in block.items:
                item.delta_arrow = 0
        for item in block.items:
                if item.arrow_to is None:
                        continue
                dest_item = block.items[item.arrow_to]
                if item.arrow_to > item.index:
                        item.delta_arrow += 1
                        dest_item.delta_arrow -= 1
                else:
                        item.delta_arrow -= 1
                        dest_item.delta_arrow += 1
        nr_arrows = 0
        for item in block.items:
                if block.previous_block:
                        item.highlight = False
                        for i in item.previous_items:
                                if i.highlight:
                                        item.highlight = True
                                        break
                if item.highlight:
                        item.fillRect()
                else:
                        item.fillText()
                item.lines_to_children()
                nr_arrows += item.delta_arrow
                item.nr_arrows = nr_arrows
                if item.arrow_to:
                        block.ctx.strokeStyle = "#000"
                        item.draw_arrow()
