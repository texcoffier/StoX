
# The following instructions pop the stack and JUMP if the test is fine:
#   JUMP !=0
#   JUMP ==0
#   JUMP <=0
#   JUMP <0
#   JUMP >=0
#   JUMP >0

# To let the lexer find '!='
LEX.call('update_lex', [100, 'negate', '[ \n\t]*[!][ \n\t]*', '#808'])

def le(cpu): cpu.stack_pop() <= 0 and cpu.set_PC(cpu.get_data_word())
def lt(cpu): cpu.stack_pop() <  0 and cpu.set_PC(cpu.get_data_word())
def ge(cpu): cpu.stack_pop() >= 0 and cpu.set_PC(cpu.get_data_word())
def gt(cpu): cpu.stack_pop() >  0 and cpu.set_PC(cpu.get_data_word())
def eq(cpu): cpu.stack_pop() == 0 and cpu.set_PC(cpu.get_data_word())
def ne(cpu): cpu.stack_pop() != 0 and cpu.set_PC(cpu.get_data_word())

reverse_operator = {'<=':  '>',  '<': '>=',
                    '>=':  '<',  '>': '<=',
                    '==': '!=', '!=': '==',
                    }

def define_operator(operator):
        def asm_operator(block, item, data):
            # If 'data' is 'None': push 0 or 1 on the stack
            # else it is ['jump on false', 'the jump label', []]
            # The [] will contains all the memory addresses
            # to patch to put the real jump address.
            t = operator
            if data:
                if data[0] == 'jump on false':
                    t = reverse_operator[t]
                label_true = data[1]
            else:
                label_true = block.new_label('compare_true')
                label_end = block.new_label('compare_end')

            asm_generate(block, item.children[0])
            asm_generate(block, item.children[1])
            asm_Item(block, item, 'SUBTRACTION', '', [], asm_feedback_binary)
            asm_Item(block, item, 'JUMP ' + t + '0',
                     label_true, asm_bytes(0xFFFF), asm_feedback_pop)
            jump_bad_addr = block.segment_code - 2

            if data:
                data[2].append(jump_bad_addr)
            else:
                asm_Item(block, item, 'LOAD_IMMEDIATE', '0', [0], asm_feedback_push)
                asm_Item(block, item, 'JUMP', label_end, asm_bytes(0xFFFF))
                jump_end_addr = block.segment_code - 2
                block.add_label(item, label_true)
                block.cpu.set_data_word(jump_bad_addr, block.segment_code)
                asm_Item(block, item, 'LOAD_IMMEDIATE', '1', [1], asm_feedback_push)
                block.add_label(item, label_end)
                block.cpu.set_data_word(jump_end_addr, block.segment_code)

        return asm_operator

for name, operator in [['le', '<='], ['ge', '>='],
                       ['eq', '=='], ['ne', '!='],
                       ['lt', '<' ], ['gt', '>' ],
                      ]:
        LEX.call('update_lex', [100 - len(operator),
                               name,
                               r'[ \n\t]*' + operator + r'[ \n\t]*',
                               '#808'])
        YAC.call('update_yac',
                 [1950, 'Binary', ['Expression', name, 'Expression']])

        fct = eval(name)
        fct.stox_name = 'JUMP ' + operator + '0'
        fct.stox_size = 2 # 2 bytes of data after instruction code
        ASM.new_instruction(fct)

        ASM.call('update_asm', [operator, define_operator(operator)])

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

