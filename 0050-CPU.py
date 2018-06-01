class CPU(Block):
        title = "Processor"
        name = "CPU"
blocks.append(CPU())

blocks.get('CPU').add_filter('dump', LEX_dump)
blocks.get('CPU').add_filter('html_init', canvas_html_init)
blocks.get('CPU').add_filter('html_draw', SRC_html_draw)

def CPU_set_time(block, t):
        asm = blocks.get('ASM')
        if t == 0:
                block.t = t
                block.items = []
                block.append(Item('PC:'))
                block.append(asm.cpu.PC)
                asm.cpu.PC.x = 3
                block.append(Item('SP:', 0, 1))
                block.append(asm.cpu.SP)
                asm.cpu.SP.y = 1
                asm.cpu.SP.x = 3
                return
        asm.cpu.step()

blocks.get('CPU').add_filter('set_time', CPU_set_time)

def ASM_one_step(block, dummy):
        block.set_time(block.t + 1)

blocks.get('CPU').add_filter('draw_cursor', ASM_one_step)


