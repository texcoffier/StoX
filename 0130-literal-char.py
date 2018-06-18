
LEX.call('update_lex',
        [90, 'literal_char', "[ \\n\\t]*'([^'\\\\]|\\\\n|\\\\t)'[ \\n\\t]*", '#880'])
LEX.call('update_lex',
        [92, 'literal_char_unterminated', "[ \\n\\t]*'.?.?", '#F00'])

YAC.call('update_yac', [400, 'ValueChar', ['literal_char']])
YAC.call('update_yac', [400, 'Value'    , ['ValueChar']])

def ast_value_char(block, item):
        item.children[0].value = str(ord(eval(item.children[0].char)))
        return AST_item(item, 'Value', [AST_item(item.children[0])])
AST.call('update_ast', ['ValueChar', ast_value_char])

def literal_char_regtest(block, item):
        block.check("put('a')", '0×0:a\n')
        block.check("put('\\n')put('F')", '0×0: \n0×1:F\n')
        block.check("put('\\t')put('F')", '0×0:\t\n1×0:F\n')
TTY.add_filter('regtest', literal_char_regtest)
