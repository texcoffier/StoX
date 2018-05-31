class SRC(Block):
        title = "Source code editor"
        name = "SRC"
        def analyse(self, text):
                self.items = []
                x = y = 0
                for char in text:
                        self.append(Item(char, x, y))
                        if char == '\n':
                                x = 0
                                y += 1
                        else:
                                x += 1
blocks.append(SRC())

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

def SRC_set(block, text):
        if not hasattr(block, 'history'):
                block.history = []
        if len(block.history) != block.t + 1:
                block.history = block.history[:block.t]
        block.history.append(text)
        block.analyse(text)
        block.t += 1
        block.next_block.set_time(0)
blocks.get('SRC').add_filter('set', SRC_set)

def SRC_set_time(block, t):
        block.t = t
        block.analyse(block.history[t])
        block.next_block.set_time(0)
blocks.get('SRC').add_filter('set_time', SRC_set_time)

def canvas_html_init(block, title):
        div = document.createElement('DIV')
        div.innerHTML = "<p>" + title + "</p><canvas></canvas>"
        div.style.display = "inline-block"
        block.blocks.element.appendChild(div)
        block.element = div.lastChild
        block.element.width = 200
        block.element.height = 500
        block.element.style.width  = str(block.element.width) + 'px'
        block.element.style.height = str(block.element.height) + 'px'
        block.ctx = block.element.getContext("2d")
blocks.get('SRC').add_filter('html_init', canvas_html_init)

def SRC_html_draw(block, dummy):
        block.ctx.fillStyle = "#FFF"
        block.ctx.clearRect(0, 0, 10000, 10000)
        block.ctx.font = str(block.fontsize) + "px monospace"

        for item in block.items:
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
blocks.get('SRC').add_filter('html_draw', SRC_html_draw)

def SRC_draw_cursor(block, dummy):
        for item in block.items:
                item.highlight = item.index == block.cursor - 1
        if not block.cursor_visible:
                return
        right = False
        if block.cursor == 0 or len(block.items) == 0:
                item = block.empty
        elif block.cursor < len(block.items):
                item = block.items[block.cursor]
        else:
                item = block.items[-1]
                right = True
        x, y = item.xy()
        w, h = item.wh()
        if right:
                if item.char == '\n':
                        y += block.fontsize
                        x = block.empty.xy()[0] + 3
                else:
                        x += w
        block.ctx.fillStyle = "#000"
        block.ctx.strokeStyle = "#F00"
        block.ctx.lineWidth = 3
        block.ctx.fillRect(x - 3, y - h, 3, block.fontsize + 2)
blocks.get('SRC').add_filter('draw_cursor', SRC_draw_cursor)

def SRC_key(blocks, event):
        if event.ctrlKey or event.metaKey or event.altKey:
                return
        key = event.key
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
                event.preventDefault(True)
                event.cancelBubble = True
        else:
                print('key=', key)
        src.cursor_visible = 1
blocks.add_filter('key', SRC_key)

def SRC_regtest(src, dummy):
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
blocks.get('SRC').add_filter('regtest', SRC_regtest)