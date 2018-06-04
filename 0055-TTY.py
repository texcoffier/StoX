class _TTY_(Block):
        title = "TTY"
        name = "TTY"
TTY = blocks.append(_TTY_())

TTY.add_filter('dump', LEX_dump)
TTY.add_filter('html_init', canvas_html_init)
TTY.add_filter('html_draw', SRC_html_draw)

def TTY_set_time(block, t):
        block.t = t
        block.items = []
        block.x = 0
        block.y = 0
        ASM.cpu.tty = block
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
