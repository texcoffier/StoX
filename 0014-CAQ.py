"""Block: course and question"""

class _CAQ_(Block):
        title = "Course &amp; Question"
        name = "CAQ"
        height = 50
        words = {}
CAQ = blocks.append(_CAQ_())
CAQ.add_filter('html_init', canvas_html_init)

def CAQ_set(block, text):
        block.items = []
        block.words = {}
        x = y = 0
        start = []
        def add(char, x, y):
                item = Item(char, x, y)
                block.append(item)
                if item.clipped():
                        x = 0
                        y += 1
                        item.x = 0
                        item.y = y
                x += len(char) + 1
                return item, x, y
        for line in text.split('\n'):
                normal = True
                for chunk in line.split("‘"):
                        if normal:
                                for char in chunk.split(' '):
                                        item, x, y = add(char, x, y)
                        else:
                                item, x, y = add(chunk, x, y)
                                if chunk not in block.words:
                                        block.words[chunk] = []
                                block.words[chunk].append(item)
                        normal = not normal
                x = 0
                y += 1
        block.set_to_minimal_height()
CAQ.add_filter('set', CAQ_set)

def CAQ_update_src(src, dummy):
        for i in CAQ.items:
                i.next_items = []
        t = src.history[-1]
        for word in CAQ.words:
                for i in range(len(t)):
                        if t[i:i+len(word)] == word:
                                for p in CAQ.words[word]:
                                        p.color = '#00F'
                                for j in range(i, i+len(word)):
                                        src.items[j].previous_items = CAQ.words[word]
def CAQ_update_highlight(block, dummy):
        for item in CAQ.items:
                if len(item.next_items) == 0:
                        continue
                item.highlight = ( item.next_items[0].index
                                   <= SRC.cursor - 1
                                   <= item.next_items[-1].index )
def CAQ_init(block, dummy):
        # After SRC.set in order to 'set previous_items' of SRC
        SRC.add_filter('set_time', CAQ_update_src)
        # After SRC.draw_cursor in order to compute 'highlight'
        SRC.add_filter('draw_cursor', CAQ_update_highlight)
        CAQ.add_filter('html_draw', SRC_html_draw)
        SRC.window_top = False
CAQ.add_filter('init', CAQ_init) # SRC is not yet created



