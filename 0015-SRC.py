class _SRC_(Block):
        title = "Source code editor"
        name = "SRC"
        time_travel = ['^Z', '^Y']
        mousemove = None
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
SRC = blocks.append(_SRC_())
SRC.add_filter('html_init', canvas_html_init)
SRC.add_filter('html_draw', SRC_html_draw)

def SRC_init(block, dummy_args):
        block.cursor_visible = 1
        block.t = -1
        block.history = []
SRC.add_filter('init', SRC_init)

def SRC_dump(block, dummy_args):
        dump_item = block.get_filter('dumpitem')
        for item in block.items:
                item.dump()
                for function in dump_item:
                        function(item)
SRC.add_filter('dump', SRC_dump)

def SRC_set(block, text):
        if len(block.history) != block.t + 1:
                block.history = block.history[:block.t+1]
        block.history.append(text)
        block.analyse(text)
        block.set_time(block.t + 1)
        block.next_block.set_time(0)
SRC.add_filter('set', SRC_set)

def SRC_cursor(block, position):
        if position > len(block.items):
                position = len(block.items)
        elif position < -1:
                position = 0
        block.cursor = position
        block.cursor_visible = 1
SRC.add_filter('cursor', SRC_cursor)

def SRC_set_time(block, t):
        if t < 0 or t >= len(block.history):
                return
        block.t = t
        block.analyse(block.history[t])
        block.call('cursor', block.cursor)
        block.next_block.set_time(0)
SRC.add_filter('set_time', SRC_set_time)

def block_set_time(block, t):
        if body and block.time_travel and block.time_travel_t:
                block.time_travel_t.innerHTML = t

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
        block.ctx.fillStyle = "#00F"
        block.ctx.fillRect(x - 2, y - h, 2, block.fontsize + 2)
SRC.add_filter('draw_cursor', SRC_draw_cursor)

def stop_event(event):
        event.preventDefault(True)
        event.cancelBubble = True

def SRC_key(blocks, event):
        if event.metaKey or event.altKey:
                return
        key = event.key
        if event.ctrlKey:
                if key == 'z':
                        SRC.set_time(SRC.t - 1)
                elif key == 'y':
                        SRC.set_time(SRC.t + 1)
                return
        cursor = SRC.cursor
        y = SRC.items[min(cursor, len(SRC.items)-1)].y
        content = SRC.history[SRC.t]
        if key == 'ArrowRight':
                cursor += 1
        elif key == 'ArrowLeft':
                cursor -= 1
        elif key == 'Home':
                while cursor > 0 and SRC.items[cursor - 1].y == y:
                        cursor -= 1
        elif key == 'End':
                while cursor < len(SRC.items)-1 and SRC.items[cursor + 1].y == y:
                        cursor += 1
                if cursor == len(SRC.items)-1 and SRC.items[-1].char != '\n':
                        cursor += 1
        elif key == 'ArrowUp' or key == 'ArrowDown':
                if cursor == len(content):
                        if content[-1] == '\n':
                                after = 0
                        else:
                                after = 1
                        item = SRC.items[-1]
                else:
                        after = 0
                        item = SRC.items[cursor]
                if key == 'ArrowUp':
                        direction = -1
                else:
                        direction = 1
                item, after = SRC.change_line(item, direction, after)
                cursor = item.index + after
        elif key == 'Backspace':
                if SRC.cursor != 0:
                        new_content = content[:cursor-1] + content[cursor:]
                        cursor -= 1
                        SRC.call('set', new_content)
        elif key == 'Delete':
                if SRC.cursor != len(content):
                        new_content = content[:cursor] + content[cursor+1:]
                        SRC.call('set', new_content)
        elif len(key) == 1 or key == 'Enter':
                if key == 'Enter':
                        key = '\n'
                new_content = content[:cursor] + key + content[cursor:]
                SRC.call('set', new_content)
                cursor += 1
        else:
                print('key=', key)
                return
        stop_event(event)
        SRC.call('cursor', cursor)
blocks.add_filter('key', SRC_key)

def SRC_mousedown(block, event):
        if SRC.mousemove is None:
                return
        cursor = SRC.mousemove.index + 1
        if event.target is not SRC.element:
                while cursor > 0 and SRC.items[cursor-1].char in [' ','\n','\t']:
                        cursor -= 1
        SRC.call('cursor', cursor)
blocks.add_filter('mousedown', SRC_mousedown)


def SRC_regtest(src, dummy):
        src.call('set', 'a\nab\na\n\na')
        src.call('set', 'a\nab\na\n\na\n')
        src.call('set', 'a\nab\na\n\na\naa\na')
        t0 = len(src.history)-3
        t1 = len(src.history)-2
        t2 = len(src.history)-1
        for t in [t0, t1, t2]:
                src.set_time(t)
                char = 0
                tests = [
                        [0,0, 2,0], [1,0, 3,0], [0,0, 5,0], [1,0, 6,0],
                        [1,0, 6,0], [2,0, 7,0], [3,0, 7,0], [5,0, 8,0]
                        ]
                if t == t0:
                        more = [[7,0, 8,0], [7,0, 8,1]]
                elif t == t1:
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
SRC.add_filter('regtest', SRC_regtest)
