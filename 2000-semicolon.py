"""Source code: tell to put an «;» between statements"""

LEX.call('update_lex',[100, 'semicolon', '[ \n\t]*[;][ \n\t]*', '#F08'])

YAC.call('update_yac',[8990,'Statement',['Statement','semicolon','Statement']])

YAC.call('update_yac',[8990,'Statement', ['Statement','Statement'],
                       [1 , 'Missing «;»']])

def ast_statement2(block, item):
        return AST_item(item, 'Statement', [ast_apply(block, child)
                                            for child in item.children
                                            if not child.error
                                            ])
AST.call('update_ast', ['Statement', ast_statement2])

