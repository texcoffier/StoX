class OBJ(Block):
        title = "Memory content"
        name = "OBJ"
blocks.append(OBJ())

blocks.get('OBJ').add_filter('dump', LEX_dump)
blocks.get('OBJ').add_filter('html_init', canvas_html_init)
blocks.get('OBJ').add_filter('html_draw', SRC_html_draw)

def OBJ_set_time(block, t):
        block.t = t
        asm = blocks.get('ASM')
        block.items = []
        n = 0
        for i in asm.cpu.code:
                block.append(i)
                i.x = 3 * (n % 4)
                i.y = n // 4
                n += 1
        n = 64
        for i in asm.cpu.heap:
                block.append(i)
                i.x = 3  * (n % 4)
                i.y = n // 4
                n += 1
        block.next_block.set_time(0)
blocks.get('OBJ').add_filter('set_time', OBJ_set_time)

