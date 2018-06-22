"""Block: the object code and memory"""

class _OBJ_(Block):
        title = "Memory content"
        name = "OBJ"
        
        def display(self, title, start, stop):
                nr = 8
                if len(self.items):
                        n = self.items[-1].y + 2
                else:
                        n = 0
                self.append(Item(title+' ['+hex4(start)+'-'+hex4(stop)+'[',
                            0, n))
                n += 2
                for i in range(start, stop):
                        line = (i-start) // nr
                        if i % nr == 0:
                                self.append(Item(hex4(i), 0, n + line))
                        item = ASM.cpu.memory[i]
                        self.append(item)
                        item.x = 4.1 + 2.1 * (i % nr)
                        item.y = n + line
OBJ = blocks.append(_OBJ_())

OBJ.add_filter('dump', LEX_dump)
OBJ.add_filter('html_init', canvas_html_init)
OBJ.add_filter('html_draw', SRC_html_draw)

def OBJ_html_draw(block, dummy):
        cpu = ASM.cpu
        if cpu.PC.value in cpu.memory:
                asm = cpu.memory[cpu.PC.value].asm
                asm.feedback(asm)
OBJ.add_filter('html_draw', OBJ_html_draw)

def OBJ_set_time(block, t):
        block.t = t
        block.items = []
        block.display("Code" , 0               , ASM.segment_code)
        block.display("Heap" , ASM.segment_heap, 0x8000)
        block.display("Stack", 0x8000          , ASM.segment_stack)
        block.next_block.call('set_time', 0)
OBJ.add_filter('set_time', OBJ_set_time)
