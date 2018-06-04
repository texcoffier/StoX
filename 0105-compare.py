
# The following instructions pop the stack and JUMP if the test is fine:
#   JUMP !=0
#   JUMP ==0
#   JUMP <=0
#   JUMP <0
#   JUMP >=0
#   JUMP >0

# To let the lexer find '!='
blocks.get('LEX').call('add_lexem',
                       [100, 'negate', '[ \n\t]*[!][ \n\t]*', '#808'])

def le(cpu): cpu.stack_pop() <= 0 and cpu.set_PC(cpu.get_data_word())
def lt(cpu): cpu.stack_pop() <  0 and cpu.set_PC(cpu.get_data_word())
def ge(cpu): cpu.stack_pop() >= 0 and cpu.set_PC(cpu.get_data_word())
def gt(cpu): cpu.stack_pop() >  0 and cpu.set_PC(cpu.get_data_word())
def eq(cpu): cpu.stack_pop() == 0 and cpu.set_PC(cpu.get_data_word())
def ne(cpu): cpu.stack_pop() != 0 and cpu.set_PC(cpu.get_data_word())

def define_operator(operator):
        def asm_operator(block, item):
            asm_generate(block, item.children[0])
            asm_generate(block, item.children[1])
            asm_Item(block, item, 'SUBTRACTION', '', [], asm_feedback_binary)
            asm_Item(block, item, 'JUMP ' + operator + '0', 'OK',
                     asm_bytes(0xFFFF), asm_feedback_pop)
            address_to_patch = block.segment_code - 2
            asm_Item(block, item, 'LOAD IMMEDIATE', '0', [0], asm_feedback_push)
            asm_Item(block, item, 'JUMP', 'COMPARE_END', asm_bytes(0xFFFF))
            block.cpu.set_data_word(address_to_patch, block.segment_code)
            address_to_patch = block.segment_code - 2
            asm_Item(block, item, 'COMPARE_OK:')
            asm_Item(block, item, 'LOAD IMMEDIATE', '1', [1], asm_feedback_push)
            asm_Item(block, item, 'COMPARE_END:')
            block.cpu.set_data_word(address_to_patch, block.segment_code)
        return asm_operator

for code, name, operator in [[0x0A, 'le', '<='],
                             [0x0B, 'ge', '>='],
                             [0x0C, 'eq', '=='],
                             [0x0D, 'ne', '!='],
                             [0x0E, 'lt', '<' ],
                             [0x0F, 'gt', '>' ],
                            ]:
        blocks.get('LEX').call('add_lexem',
                               [100 - len(operator),
                                name,
                                r'[ \n\t]*' + operator + r'[ \n\t]*',
                                '#808'])
        blocks.get('YAC').call('update_rule',
            [1950, 'Binary', [['Expression'], [name], ['Expression']]])

        Instruction(code, 'JUMP ' + operator + '0', 2, eval(name))

        blocks.get('ASM').call('update_rule', 
                               [operator, define_operator(operator)])

def compare_regtest(tty, dummy):
        asm = blocks.get('ASM')
        src = blocks.get('SRC')
        def set_source(i, operator, j, expected):
                src.call('set', 'put(48 + (' + str(i) + operator + str(j) +'))')
                for k in range(9):
                        asm.cpu.step()
                if (tty.items[0].char != '0') != expected:
                        print('computed:', tty.items[0].char)
                        print('expected:', expected)
                        bug
        for i in [5, 6, 7]:
                for j in [5, 6, 7]:
                        for operator in ['<', '>', '<=', '>=', '==', '!=']:
                                set_source(i, operator, j,
                                           eval('i' + operator + 'j'))
blocks.get('TTY').add_filter('regtest', compare_regtest)

