
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
        def asm_operator(block, item):
            BCS.begin()
            asm_generate(block, item.children[0])
            asm_generate(block, item.children[1])
            asm_Item(block, item, 'SUBTRACTION', '', [], asm_feedback_binary)
            BCS.jump_false(item, reverse_operator[operator])
            BCS.jump_true(item)
            BCS.end(item)

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
        print("Comparator regtest")
        def set_source(i, operator, j, expected):
                if expected:
                    c = '1'
                else:
                    c = '0'
                tty.check('put(48 + (' + str(i) + operator + str(j) +'))',
                          '0×0:' + c + '\n')
        for i in [5, 6, 7]:
                for j in [5, 6, 7]:
                        for operator in ['<', '>', '<=', '>=', '==', '!=']:
                                set_source(i, operator, j,
                                           eval('i' + operator + 'j'))
TTY.add_filter('regtest', compare_regtest)

