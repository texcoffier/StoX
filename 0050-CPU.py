"""Block: the processor and its registers"""

class _CPU_(Block):
        title = "Processor"
        name = "CPU"
        height = 30
        time_travel = ['⇞', '⇟']
CPU = blocks.append(_CPU_())

CPU.add_filter('dump', LEX_dump)
CPU.add_filter('html_init', canvas_html_init)
CPU.add_filter('html_draw', SRC_html_draw)

def CPU_set_time(block, t):
        asm = ASM
        if t < 0:
                t = 0
        if t <= block.t:
                block.t = 0
                block.items = []
                block.append(Item('PC:'))
                block.append(asm.cpu.PC)
                asm.cpu.PC.x = 3
                block.append(Item('SP:', 0, 1))
                block.append(asm.cpu.SP)
                asm.cpu.SP.y = 1
                asm.cpu.SP.x = 3
                asm.cpu.reset()
                block.next_block.call('set_time', 0)
                block.set_to_minimal_height()
        while block.t < t:
                if not asm.cpu.step():
                        break
                block.t += 1
CPU.add_filter('set_time', CPU_set_time)

def CPU_regtest(block, dummy):
        asm = ASM
        for input, output in [
                ['a=1'          ,    1],
                ['a=-1'         ,   -1],
                ['a=128'        , -128],
                ['a=8-2'        ,    6],
                ['a=2-8'        ,   -6],
                ['a=127+1'      , -128],
                ['a=-128-1'     ,  127],
        ]:
                SRC.call('set', input)
                asm.cpu.run()
                computed = asm.cpu.memory[asm.segment_heap].value
                if computed != output:
                        print("input:", input)
                        print("expected:", output)
                        print("computed:", computed)
                        print(asm.cpu.memory[asm.segment_heap].long())
                        bug
CPU.add_filter('regtest', CPU_regtest)
