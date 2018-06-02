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

def CPU_one_step(block, dummy):
        block.set_time(block.t + 1)
blocks.get('CPU').add_filter('draw_cursor', CPU_one_step)

def CPU_regtest(block, dummy):
        asm = blocks.get('ASM')
        for input, output in [
                ['a=1'          ,    1],
                ['a=-1'         ,   -1],
                ['a=128'        , -128],
                ['a=8-2'        ,    6],
                ['a=2-8'        ,   -6],
                ['a=127+1'      , -128],
                ['a=-128-1'     ,  127],
        ]:
                blocks.get('SRC').call('set', input)
                for i in range(100):
                        CPU_one_step(block, None)
                computed = asm.cpu.memory[asm.segment_heap].value
                if computed != output:
                        print("input:", input)
                        print("expected:", output)
                        print("computed:", computed)
                        print(asm.cpu.memory[asm.segment_heap].long())
                        bug
blocks.get('CPU').add_filter('regtest', CPU_regtest)

