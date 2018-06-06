
# What:           Loop
# Syntax:         while(expression) { instructions }
# Generated code:
#      WHILE_START_0:
#      expression code
#      JUMP IF ZERO WHILE_END_0
#      instructions
#      JUMP WHILE_START_0

##############################################################################
# Lexical analyser
##############################################################################

LEX.call('add_lexem',
        [90,      # Priority: must be higher than the 'word' lexem priority
         'while',                 # Name
         '[ \n\t]*while[ \n\t]*', # Regular expression to match
         '#480'   # Color
        ])
LEX.call('add_lexem',
        [100,
         'open-brace', # Name
         ' *[{] *'   , # Regular expression to match
         '#480'        # Color
        ])
LEX.call('add_lexem',
        [100,
         'close-brace', # Name
         ' *[}] *'    , # Regular expression to match
         '#480'         # Color
        ])

##############################################################################
# Syntaxic analyser
##############################################################################

YAC.call('update_rule',
        [450,   # Before the promotion of 'Group' to 'Value'
         'While', # Name
         [['while'], ['Expression'], ['open-brace'],['Statement'],['close-brace']]
        ])
# 'While' is a 'Statement'
YAC.call('update_rule', [8000, 'Statement', [['While']]])

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
AST.call('update_rule', ['While', ast_while])

##############################################################################
# Add processor 'JUMP' instruction
##############################################################################

def JUMP(cpu):
        cpu.set_PC(cpu.get_data_word())
Instruction("JUMP", 2, JUMP)

##############################################################################
# Generate assembly code
##############################################################################

def asm_while(block, item):
        label_start  = block.new_label('while_start')
        label_end    = block.new_label('while_end')

        while_start = block.segment_code
        block.add_label(item, label_start)
        # The generate assembly will let the expression result on the stack
        asm_generate(block, item.children[0])
        # Stop the loop if zero
        asm_Item(block,
                 item,             # Take color/highlightcursor from AST 'While'
                 'JUMP ==0',       # Processor instruction
                 label_end,        # Instruction parameter (only for user feedback)
                 asm_bytes(0xFFFF),# Data byte to put after instruction code
                 asm_feedback_pop  # Rectangle feedback on execution
                 )
        address_to_patch = block.segment_code - 2
        # The loop code
        asm_generate(block, item.children[1])
        asm_Item(block,
                 item,            # Take color/highlightcursor from AST 'While'
                 'JUMP',          # Processor instruction
                 label_start,    # Instruction parameter (only for user feedback)
                 asm_bytes(while_start)
                 )
        block.add_label(item, label_end)
        block.cpu.set_data_word(address_to_patch, block.segment_code)
ASM.call('update_rule',
                        ['While',   # AST node name
                         asm_while  # Generating function
                         ])

##############################################################################
# Regression tests
##############################################################################

def while_regtest(tty, dummy):
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
TTY.add_filter('regtest', while_regtest)

