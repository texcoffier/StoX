

LEX.call('update_lex',
        [100,                  # Priority: must be higher than the 'word' lexem priority
         'boolean_and'       , # Name
         '[ \n\t]*&&[ \n\t]*', # Regular expression to match
         '#808'                # Color
        ])
LEX.call('update_lex',
        [100,                     # Priority: must be higher than the 'word' lexem priority
         'boolean_or'           , # Name
        '[ \n\t]*[|][|][ \n\t]*', # Regular expression to match
         '#808'                   # Color
        ])


YAC.call('update_yac',
        [2010,     # Less priority than relational operators
         'Binary', # Name
         ['Expression', 'boolean_and', 'Expression'],
        ])
YAC.call('update_yac',
        [2011,    # Less priority than relational operators
         'Binary', # Name
         ['Expression', 'boolean_or', 'Expression'],
        ])

def asm_boolean_or(block, item):
        label_or = ASM.new_label('bool_or')
        BCS.begin(None, label_or)
        asm_generate(block, item.children[0])
        BCS.jump_true(item, '!=')

        ASM.add_label(item, label_or)
        if BCS.stack[-2].label_false:
                BCS.stack[-1].label_false = BCS.stack[-2].label_false
        else:
                BCS.stack[-1].label_false = ASM.new_label('bool_false')
        asm_generate(block, item.children[1])
        BCS.jump_true(item, '!=')
        BCS.end(item)
ASM.call('update_asm', ['||', asm_boolean_or])

def asm_boolean_and(block, item):
        label_and = ASM.new_label('bool_and')
        BCS.begin(label_and)
        asm_generate(block, item.children[0])
        BCS.jump_false(item, '==')

        ASM.add_label(item, label_and)
        if BCS.stack[-2].label_true:
                BCS.stack[-1].label_true = BCS.stack[-2].label_true
        else:
                BCS.stack[-1].label_true = ASM.new_label('bool_true')
        asm_generate(block, item.children[1])
        BCS.jump_false(item, '==')
        BCS.end(item)
ASM.call('update_asm', ['&&', asm_boolean_and])

def boolean_regtest(tty, dummy):
        print("Boolean regtest")
        for x in ["2==2", "2==3"]:
         for y in ["4==4", "4==5"]:
          for z in ["6==6", "6==7"]:
                f = x + '||' + y + '||' + z
                if f == '2==3||4==5||6==7':
                        v = '0'
                else:
                        v = '1'
                tty.check('put(48 + (' + f + '))', '0×0:' + v + '\n')
                f = x + '&&' + y + '&&' + z
                if f == '2==2&&4==4&&6==6':
                        v = '1'
                else:
                        v = '0'
                tty.check('put(48 + (' + f + '))', '0×0:' + v + '\n')
                
        tty.check('put(48 + (1==1&&2==2||3==4&&5==6))', '0×0:1\n')
        tty.check('put(48 + (1==1&&2==3||4==4&&5==6))', '0×0:0\n')
        tty.check('put(48 + (1==2&&2==2||3==4&&5==5))', '0×0:0\n')
        tty.check('put(48 + ((1==2||2==2)&&(3==2||5==5)))', '0×0:1\n')
        tty.check('put(48 + ((1==2||2==3)&&(3==2||5==5)))', '0×0:0\n')
        tty.check('put(48 + ((1==2||2==2)&&(3==2||5==6)))', '0×0:0\n')
#TTY.add_filter('regtest', boolean_regtest)

