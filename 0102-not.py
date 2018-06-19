"""Source code: the operators «!» and «~» as boolean and binary «not»"""

LEX.call('update_lex', [100, 'negate', '[ \n\t]*[~!][ \n\t]*', '#808'])

YAC.call('update_yac',
        [1250,    # same priority than unary + and -
         'Negate', # Name
         ['negate', 'Expression'],
        ])
YAC.call('update_yac',
        [1251,    # same priority than unary + and -
         'Expression', ['Negate'],
        ])

def ast_negate(block, item):
        node = ast_apply(block, item.children[1])
        return AST_item(item.children[0], None, [node])
AST.call('update_ast', ['Negate', ast_negate])

# NOT boolean

def asm_boolean_negate(block, item):
        BCS.begin()
        f = BCS.stack[-1].label_false
        t = BCS.stack[-1].label_true
        BCS.stack[-1].label_false = t
        BCS.stack[-1].label_true = f
        asm_generate(block, item.children[0])
        BCS.jump_true(item, '==')
        BCS.jump_false(item)
        BCS.end(item)
ASM.call('update_asm', ['!', asm_boolean_negate])

# NOT binary

def COMPLEMENT(cpu): cpu.stack_push(~cpu.stack_pop())
ASM.new_instruction(COMPLEMENT)

def asm_binary_negate(block, item):
        asm_generate(block, item.children[0])
        asm_Item(block, item, 'COMPLEMENT', '', [], asm_feedback_unary)
ASM.call('update_asm', ['~', asm_binary_negate])

# Remove double binary complement

def OPT_complement(item):
        if (item.rule == 'negate' and item.value == '~'
            and item.children[0].rule == 'negate'
            and item.children[0].value == '~'):
                return item.children[0].children[0]
OPT.call('update_opt', OPT_complement)

# Regression tests

def negate_regtest(tty, dummy):
        print("Negate regtest")
        for value, expected in [
                ['put(!0+65)', '0×0:B\n'],
                ['put(!2+65)', '0×0:A\n'],
                ['put(!!2+65)', '0×0:B\n'],
                ['put(66+~0)', '0×0:A\n'],
                ['put(66+~-1)', '0×0:B\n'],
                ['put(68+~2)', '0×0:A\n'],
                ['put(~~65)', '0×0:A\n'],
                ]:
                tty.check(value, expected)
TTY.add_filter('regtest', negate_regtest)
