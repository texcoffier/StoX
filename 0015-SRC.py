class _SRC_(Block):
        title = "Source code editor"
        name = "SRC"
        time_travel = ['^Z', '^Y']
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

def SRC_set_time(block, t):
        if t < 0 or t >= len(block.history):
                return
        block.t = t
        block.analyse(block.history[t])
        if block.cursor > len(block.items):
                block.cursor = len(block.items)
        block.next_block.set_time(0)
SRC.add_filter('set_time', SRC_set_time)

def canvas_html_init(block, title):
        div = document.createElement('DIV')
        div.innerHTML = ('<p class="title">'
                         + title
                         + '</p>'
                         + '<canvas></canvas>'
                         + '<div class="footer"></div>')
        div.style.display = "inline-block"
        div.style.verticalAlign = 'top'
        block.blocks.element.appendChild(div)
        if block.time_travel:
                tt = div.childNodes[2]
                tt.innerHTML = (
                          '<button>◀ ' + block.time_travel[0] + '</button>'
                        + '<span></span>'
                        + '<button>' + block.time_travel[1] + ' ▶</button>'
                        )
                block.time_travel_t = tt.childNodes[1]
                def time_travel_back():
                        block.set_time(block.t - 1)
                def time_travel_forward():
                        block.set_time(block.t + 1)
                tt.childNodes[0].onclick = time_travel_back
                tt.childNodes[2].onclick = time_travel_forward
        block.element = div.childNodes[1]
        block.element.width = (4 * window_width) / len(blocks.blocks)
        block.element.height = window_height - 100
        block.element.style.width = str(block.element.width) + 'px'
        block.element.style.height = str(block.element.height) + 'px'
        block.ctx = block.element.getContext("2d")
        div.style.overflow = 'hidden'
        div.style.width = str((window_width - 50) / len(blocks.blocks)) + 'px'
        div.style.height = str(block.element.height + 100) + 'px'
SRC.add_filter('html_init', canvas_html_init)

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
SRC.add_filter('html_draw', SRC_html_draw)

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
        content = SRC.history[SRC.t]
        if key == 'ArrowRight':
                if SRC.cursor < len(content):
                        SRC.cursor += 1
                stop_event(event)
        elif key == 'ArrowLeft':
                if SRC.cursor > 0:
                        SRC.cursor -= 1
        elif key == 'Home':
                y = SRC.items[min(SRC.cursor, len(SRC.items)-1)].y
                while SRC.cursor > 0 and SRC.items[SRC.cursor-1].y == y:
                        SRC.cursor -= 1
                stop_event(event)
        elif key == 'End':
                y = SRC.items[min(SRC.cursor, len(SRC.items)-1)].y
                while SRC.cursor < len(SRC.items)-1 and SRC.items[SRC.cursor+1].y == y:
                        SRC.cursor += 1
                if SRC.cursor == len(SRC.items)-1 and SRC.items[-1].char != '\n':
                        SRC.cursor += 1
                stop_event(event)
        elif key == 'ArrowUp' or key == 'ArrowDown':
                if SRC.cursor == len(content):
                        if content[-1] == '\n':
                                after = 0
                        else:
                                after = 1
                        item = SRC.items[-1]
                else:
                        after = 0
                        item = SRC.items[SRC.cursor]
                if key == 'ArrowUp':
                        direction = -1
                else:
                        direction = 1
                item, after = SRC.change_line(item, direction, after)
                SRC.cursor = item.index + after
                stop_event(event)
        elif key == 'Backspace':
                if SRC.cursor != 0:
                        new_content = content[:SRC.cursor-1] + content[SRC.cursor:]
                        SRC.cursor -= 1
                        SRC.call('set', new_content)
        elif key == 'Delete':
                if SRC.cursor != len(content):
                        new_content = content[:SRC.cursor] + content[SRC.cursor+1:]
                        SRC.call('set', new_content)
        elif len(key) == 1 or key == 'Enter':
                if key == 'Enter':
                        key = '\n'
                new_content = content[:SRC.cursor] + key + content[SRC.cursor:]
                SRC.call('set', new_content)
                SRC.cursor += 1
                stop_event(event)
        else:
                print('key=', key)
        SRC.cursor_visible = 1
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
SRC.add_filter('regtest', SRC_regtest)
