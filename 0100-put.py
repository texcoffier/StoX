
# What:           Display one char on TTY
# Syntax:         put(ascii code)
# Generated code: PUT

##############################################################################
# Lexical analyser
##############################################################################

blocks.get('LEX').call('add_lexem',
        [90,          # Priority: must be higher than the 'word' lexem priority
         'put'                , # Name
         '[ \n\t]*put[ \n\t]*', # Regular expression to match
         '#0F0'                 # Color
        ])

##############################################################################
# Syntaxic analyser
##############################################################################

blocks.get('YAC').call('update_rule',
        [450,   # Before the promotion of 'Group' to 'Value'
         'Put', # Name
         [['put'], ['Group']] # Lexem 'put' followed by '(expression)'
        ])
# 'Put' is a 'Statement'
blocks.get('YAC').call('update_rule', [8000, 'Statement', [['Put']]])

##############################################################################
# Abstract syntax tree
##############################################################################

def ast_put(block, item):
        return AST_item(
                item.children[0], # Take color/highlightcursor from YAC 'put' lexem
                "Put",            # Name in the AST tree
                # The children of the AST node (only one here)
                [ast_apply(block, item.children[1])]
                )
blocks.get('AST').call('update_rule', ['Put', ast_put])

##############################################################################
# Add processor 'PUT' instruction
##############################################################################

def x08(cpu):
        # Execute the instruction
        blocks.get('TTY').call('put', cpu.stack_pop())

# Add the instruction to the CPU instruction set.
Instruction(0x08,    # Instruction byte code
            "PUT",   # Instruction in assembly
            0,       # ZERO byte of data after instruction code
            x08)     # The function emulating the processor instruction

##############################################################################
# Generate assembly code
##############################################################################

def asm_put(block, item):
        # The generate assembly will let result on stack
        asm_generate(block, item.children[0])
        # The 'PUT' will pop the stack top.
        asm_Item(block,
                 item,  # Take color/highlightcursor from AST 'Put'
                 'PUT', # Processor instruction
                 '',    # Instruction parameter (only for user feedback)
                 [],    # Data byte to put after instruction code
                 asm_feedback_pop # Rectangle feedback on execution
                 )
blocks.get('ASM').call('update_rule',
                        ['Put',   # AST node name
                         asm_put  # Generating function
                         ])

##############################################################################
# Regression tests
##############################################################################

def put_regtest(tty, dummy):
        blocks.get('SRC').call('set', 'put(65)put(10)\nput(66)put(67)')
        for i in range(100):
                blocks.get('ASM').cpu.step()
        for i, expect in enumerate(['0×0:A<A>,previous=8×2:08<put>',
                                    '1×0: < >,previous=14×2:08<put>',
                                    '0×1:B<B>,previous=4×3:08<put>',
                                    '1×1:C<C>,previous=10×3:08<put>']):
                if tty.items[i].long() != expect:
                        print(tty.items[i].long())
                        bug
blocks.get('TTY').add_filter('regtest', put_regtest)
