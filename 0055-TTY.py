class TTY(Block):
        title = "TTY"
        name = "TTY"
blocks.append(TTY())

blocks.get('TTY').add_filter('dump', LEX_dump)
blocks.get('TTY').add_filter('html_init', canvas_html_init)
blocks.get('TTY').add_filter('html_draw', SRC_html_draw)

def TTY_set_time(block, t):
        block.t = t
        block.items = []
        block.x = 0
        block.y = 0
        asm = blocks.get('ASM')
        asm.cpu.tty = block
blocks.get('TTY').add_filter('set_time', TTY_set_time)

def TTY_put(tty, code):
        if code == 13 or code == 10:
                display = 32
        else:
                display = code
        asm = blocks.get('ASM')
        previous = asm.cpu.memory[asm.cpu.PC.value]
        tty.append(Item(chr(display), block.x, block.y, [previous]))
        # tty.items[-1].color = "#" + hex(r) + hex(g) + hex(b)
        if code == 13:
                block.x = 0
        elif code == 10:
                block.x = 0
                block.y += 1
        else:
                block.x += 1
blocks.get('TTY').add_filter('put', TTY_put)
