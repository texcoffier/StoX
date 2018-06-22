"""Block: the screen"""

class _TTY_(Block):
        title = "TTY (screen)"
        name = "TTY"
        is_running = False
        time_travel = ['F11', 'F12']
        window_top = False
        def string(self):
                s = ''
                for item in self.items:
                        s += (str(int(item.x)) + '×' + str(int(item.y)) + ':'
                              + item.char + '\n')
                return s
        def check(self, source, expected):
                SRC.call('set', source)
                # print(source) ; ASM.call('dump')
                ASM.cpu.run()
                if expected != self.string():
                        print('=== source ===')
                        print(repr(source))
                        print('=== computed ===')
                        print(repr(self.string()))
                        print('=== expected ===')
                        print(repr(expected))
                        ASM.call('dump')
                        OBJ.call('dump')
                        bug
TTY = blocks.append(_TTY_())

TTY.add_filter('dump', LEX_dump)
TTY.add_filter('html_init', canvas_html_init)
TTY.add_filter('html_draw', SRC_html_draw)

def TTY_set_time(block, t):
        if block.is_running:
                return
        block.is_running = True
        if t == 0 or t < block.t:
                block.items = []
                block.x = 0
                block.y = 0
                ASM.cpu.tty = block
        if t < block.t:
                CPU.call('set_time', 0)
        while len(block.items) < t:
                tt = CPU.t
                CPU.call('set_time', CPU.t + 1)
                if tt == CPU.t:
                        break
        block.t = t
        block.is_running = False
TTY.add_filter('set_time', TTY_set_time)

def TTY_put(block, code):
        if code == 13 or code == 10:
                display = 32
        else:
                display = code
        previous = ASM.cpu.memory[ASM.cpu.PC.value]
        block.append(Item(chr(display), block.x, block.y, [previous]))
        if code == 13:
                block.x = 0
        elif code == 10:
                block.x = 0
                block.y += 1
        else:
                block.x += 1
TTY.add_filter('put', TTY_put)

TTY_key_codes = {'F11': -1, 'F12': +1}
def TTY_key(blocks, event):
        if event.key in TTY_key_codes:
                TTY.call('set_time', TTY.t + TTY_key_codes[event.key])
                stop_event(event)
blocks.add_filter('key', TTY_key)

