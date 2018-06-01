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
        for i in range(0, asm.segment_code):
                item = asm.cpu.memory[i]
                block.append(item)
                item.x = 3 * (n % 4)
                item.y = n // 4
                n += 1
        n = 64 - (0x8000 - asm.segment_heap + 1)
        for i in range(asm.segment_heap, 0x8000):
                n += 1
                item = asm.cpu.memory[i]
                block.append(item)
                item.x = 3  * (n % 4)
                item.y = n // 4
        n = 64
        for i in range(0x8000, asm.segment_stack):
                item = asm.cpu.memory[i]
                block.append(item)
                item.x = 3  * (n % 4)
                item.y = n // 4
                n += 1

        block.next_block.set_time(0)
blocks.get('OBJ').add_filter('set_time', OBJ_set_time)

