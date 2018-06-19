"""Source code: the «while» statement"""

# What:           Loop
# Syntax:         while(expression) { instructions }

##############################################################################
# Lexical analyser
##############################################################################

LEX.call('update_lex',
        [90,      # Priority: must be higher than the 'word' lexem priority
         'while',                 # Name
         '[ \n\t]*while[ \n\t]*', # Regular expression to match
         '#480'   # Color
        ])
LEX.call('update_lex',
        [100,
         'open-brace', # Name
         ' *[{] *'   , # Regular expression to match
         '#480'        # Color
        ])
LEX.call('update_lex',
        [100,
         'close-brace', # Name
         ' *[}] *'    , # Regular expression to match
         '#480'         # Color
        ])

##############################################################################
# Syntaxic analyser
##############################################################################

YAC.call('update_yac',
        [450,   # Before the promotion of 'Group' to 'Value'
         'While', # Name
         ['while', 'Expression', 'open-brace', 'Statement', 'close-brace']
        ])
# 'While' is a 'Statement'
YAC.call('update_yac', [8000, 'Statement', ['While']])

##############################################################################
# Abstract syntax tree
##############################################################################

def ast_while(block, item):
        return AST_item(
                item.children[0], # Take color/highlightcursor from YAC 'while' lexem
                "While",    # Name in the AST tree
                [ast_apply(block, item.children[1]),
                 ast_apply(block, item.children[3])]
                )
AST.call('update_ast', ['While', ast_while])

##############################################################################
# Add processor 'JUMP' instruction
##############################################################################

def JUMP(cpu):
        cpu.set_PC(cpu.get_data_word())
JUMP.stox_size = 2 # 2 bytes of data after instruction code
ASM.new_instruction(JUMP) # Add the instruction to the CPU instruction set

##############################################################################
# Generate assembly code
##############################################################################

def asm_while(block, item):
        BCS.begin(None, None, False)

        label_start = ASM.new_label('while_start')
        ASM.add_label(item, label_start)
        asm_generate(block, item.children[0])
        BCS.jump_false(item, '==') # Generate jump code only if it is needed

        BCS.add_label_true(item)
        asm_generate(block, item.children[1])
        block.add_jump(item, label_start)

        BCS.add_label_false(item)
        BCS.end(item)
ASM.call('update_asm',
                        ['While',   # AST node name
                         asm_while  # Generating function
                         ])

##############################################################################
# Regression tests
##############################################################################

def while_regtest(tty, dummy):
        print("While regtest")
        tty.check('while(0) { put(65) }', '')
        tty.check('a=2 while(a) { put(65)  a = a - 1 }',
                  '0×0:A\n1×0:A\n')
        tty.check('a=2 while(a != 0) { put(66)  a = a - 1 }',
                  '0×0:B\n1×0:B\n')
TTY.add_filter('regtest', while_regtest)

