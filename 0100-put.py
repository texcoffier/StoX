
# What:           Display one char on TTY
# Syntax:         put(ascii code)
# Generated code: PUT

##############################################################################
# Lexical analyser
##############################################################################

LEX.call('add_lexem',
        [90,          # Priority: must be higher than the 'word' lexem priority
         'put'                , # Name
         '[ \n\t]*put[ \n\t]*', # Regular expression to match
         '#0F0'                 # Color
        ])

##############################################################################
# Syntaxic analyser
##############################################################################

YAC.call('update_yac',
        [450,   # Before the promotion of 'Group' to 'Value'
         'Put', # Name
         ['put', 'Group'] # Lexem 'put' followed by '(expression)'
        ])
# 'Put' is a 'Statement'
YAC.call('update_yac', [8000, 'Statement', ['Put']])

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
AST.call('update_ast', ['Put', ast_put])

##############################################################################
# Add processor 'PUT' instruction
##############################################################################

def PUT(cpu):
        # Execute the instruction
        TTY.call('put', cpu.stack_pop())
PUT.stox_size = 0 # ZERO byte of data after instruction code (default value)
ASM.new_instruction(PUT) # Add the instruction to the CPU instruction set

##############################################################################
# Generate assembly code
##############################################################################

def asm_put(block, item):
        # The generated assembly code will let the result on the stack
        asm_generate(block, item.children[0])
        # The 'PUT' will pop the stack top.
        asm_Item(block,
                 item,  # Take color/highlightcursor from AST 'Put'
                 'PUT', # Processor instruction
                 '',    # Instruction parameter (only for user feedback)
                 [],    # Data bytes to put after instruction code
                 asm_feedback_pop # Rectangle feedback on execution
                 )
ASM.call('update_asm',
                        ['Put',   # AST node name
                         asm_put  # Generating function
                         ])

##############################################################################
# Regression tests
##############################################################################

def put_regtest(tty, dummy):
        SRC.call('set', 'put(65)put(10)\nput(66)put(67)')
        for i in range(100):
                ASM.cpu.step()
        for i, expect in enumerate(['0×0:A<A>,previous=8×2:08<put>',
                                    '1×0: < >,previous=14×2:08<put>',
                                    '0×1:B<B>,previous=4×3:08<put>',
                                    '1×1:C<C>,previous=10×3:08<put>']):
                if tty.items[i].long() != expect:
                        print(tty.items[i].long())
                        bug
TTY.add_filter('regtest', put_regtest)
