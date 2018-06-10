LEX.call('update_lex', [100, 'binary_or' , '[ \n\t]*[|][ \n\t]*', '#808'])
LEX.call('update_lex', [100, 'binary_and', '[ \n\t]*[&][ \n\t]*', '#808'])
LEX.call('update_lex', [100, 'binary_xor', '[ \n\t]*\\^[ \n\t]*'  , '#808'])

YAC.call('update_yac',[2010,'Binary',['Expression','binary_and','Expression']])
YAC.call('update_yac',[2011,'Binary',['Expression','binary_xor','Expression']])
YAC.call('update_yac',[2012,'Binary',['Expression','binary_or' ,'Expression']])


def AND(cpu): cpu.stack_push(cpu.stack_pop() & cpu.stack_pop())
def XOR(cpu): cpu.stack_push(cpu.stack_pop() ^ cpu.stack_pop())
def  OR(cpu): cpu.stack_push(cpu.stack_pop() | cpu.stack_pop())

ASM.new_instruction(AND)
ASM.new_instruction(XOR)
ASM.new_instruction(OR)

def asm_binary_and(block, item, data):
        asm_generate(block, item.children[0])
        asm_generate(block, item.children[1])
        asm_Item(block, item, 'AND', '', [], asm_feedback_binary)
def asm_binary_xor(block, item, data):
        asm_generate(block, item.children[0])
        asm_generate(block, item.children[1])
        asm_Item(block, item, 'XOR', '', [], asm_feedback_binary)
def asm_binary_or(block, item, data):
        asm_generate(block, item.children[0])
        asm_generate(block, item.children[1])
        asm_Item(block, item, 'OR', '', [], asm_feedback_binary)


ASM.call('update_asm', ["&", asm_binary_and])
ASM.call('update_asm', ["|", asm_binary_or])
ASM.call('update_asm', ["^", asm_binary_xor])

def binary_regtest(tty, dummy):
        print("Binary regtest")
        for op1 in ['&', '|', '^']:
         for op2 in ['&', '|', '^']:
          for op3 in ['&', '|', '^']:
           for op4 in ['&', '|', '^']:
            expr = '1' + op1 + '2' + op2 + '4' + op3 + '8' + op4 + '16'
            result = chr(eval(expr))
            tty.check('put(' + expr + ')', '0×0:' + result + '\n')
TTY.add_filter('regtest', binary_regtest)
