class OBJ(Block):
        title = "Memory content"
        name = "OBJ"
        
        def display(self, title, start, stop):
                nr = 8
                asm = blocks.get('ASM')
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
                        item = asm.cpu.memory[i]
                        self.append(item)
                        item.x = 4.1 + 2.1 * (i % nr)
                        item.y = n + line
blocks.append(OBJ())

blocks.get('OBJ').add_filter('dump', LEX_dump)
blocks.get('OBJ').add_filter('html_init', canvas_html_init)
blocks.get('OBJ').add_filter('html_draw', SRC_html_draw)


def OBJ_set_time(block, t):
        block.t = t
        block.items = []
        asm = blocks.get('ASM')
        block.display("Code" , 0               , asm.segment_code)
        block.display("Heap" , asm.segment_heap, 0x8000)
        block.display("Stack", 0x8000          , asm.segment_stack)
        block.next_block.set_time(0)
blocks.get('OBJ').add_filter('set_time', OBJ_set_time)
