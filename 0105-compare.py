
# The following instructions pop the stack and JUMP if the test is fine:
#   JUMP !=0
#   JUMP ==0
#   JUMP <=0
#   JUMP <0
#   JUMP >=0
#   JUMP >0

# To let the lexer find '!='
LEX.call('add_lexem', [100, 'negate', '[ \n\t]*[!][ \n\t]*', '#808'])

def le(cpu): cpu.stack_pop() <= 0 and cpu.set_PC(cpu.get_data_word())
def lt(cpu): cpu.stack_pop() <  0 and cpu.set_PC(cpu.get_data_word())
def ge(cpu): cpu.stack_pop() >= 0 and cpu.set_PC(cpu.get_data_word())
def gt(cpu): cpu.stack_pop() >  0 and cpu.set_PC(cpu.get_data_word())
def eq(cpu): cpu.stack_pop() == 0 and cpu.set_PC(cpu.get_data_word())
def ne(cpu): cpu.stack_pop() != 0 and cpu.set_PC(cpu.get_data_word())

def define_operator(operator):
        def asm_operator(block, item):
            label_ok  = block.new_label('compare_ok')
            label_end = block.new_label('compare_end')

            asm_generate(block, item.children[0])
            asm_generate(block, item.children[1])
            asm_Item(block, item, 'SUBTRACTION', '', [], asm_feedback_binary)
            asm_Item(block, item, 'JUMP ' + operator + '0', label_ok,
                     asm_bytes(0xFFFF), asm_feedback_pop)
            address_to_patch = block.segment_code - 2
            asm_Item(block, item, 'LOAD_IMMEDIATE', '0', [0], asm_feedback_push)
            asm_Item(block, item, 'JUMP', label_end, asm_bytes(0xFFFF))

            block.add_label(item, label_ok)
            block.cpu.set_data_word(address_to_patch, block.segment_code)
            address_to_patch = block.segment_code - 2
            asm_Item(block, item, 'LOAD_IMMEDIATE', '1', [1], asm_feedback_push)

            block.add_label(item, label_end)
            block.cpu.set_data_word(address_to_patch, block.segment_code)
        return asm_operator

for name, operator in [['le', '<='], ['ge', '>='],
                       ['eq', '=='], ['ne', '!='],
                       ['lt', '<' ], ['gt', '>' ],
                      ]:
        LEX.call('add_lexem', [100 - len(operator),
                               name,
                               r'[ \n\t]*' + operator + r'[ \n\t]*',
                               '#808'])
        YAC.call('update_rule',
            [1950, 'Binary', ['Expression', name, 'Expression']])

        fct = eval(name)
        fct.stox_name = 'JUMP ' + operator + '0'
        fct.stox_size = 2 # 2 bytes of data after instruction code
        ASM.new_instruction(fct)

        ASM.call('update_rule', [operator, define_operator(operator)])

def compare_regtest(tty, dummy):
        def set_source(i, operator, j, expected):
                SRC.call('set', 'put(48 + (' + str(i) + operator + str(j) +'))')
                for k in range(9):
                        ASM.cpu.step()
                if (TTY.items[0].char != '0') != expected:
                        print('computed:', TTY.items[0].char)
                        print('expected:', expected)
                        ASM.dump()
                        bug
        for i in [5, 6, 7]:
                for j in [5, 6, 7]:
                        for operator in ['<', '>', '<=', '>=', '==', '!=']:
                                set_source(i, operator, j,
                                           eval('i' + operator + 'j'))
TTY.add_filter('regtest', compare_regtest)

