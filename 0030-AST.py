"""Block: Abstract Syntax Tree"""

class _AST_(Block):
        title = "Abstract Syntax Tree"
        name = "AST"
        fullline_highlight = True
AST = blocks.append(_AST_())

AST.add_filter('dump', LEX_dump)
AST.add_filter('html_init', canvas_html_init)
AST.add_filter('html_draw', SRC_html_draw)

def AST_item(previous, name=None, children=[]):
        item = previous.clone()
        if name:
                item.char = name
        item.children = children
        return item

def AST_init(block, dummy):
        block.rules = {}
        for rule in [
                ['Affectation', ast_affectation],
                ['Unary'      , ast_unary],
                ['Variable'   , ast_variable],
                ['Binary'     , ast_binary],
                ['Value'      , ast_value],
                ['Group'      , ast_group],
                ['Statement'  , ast_program],
                ]:
                AST.call('update_ast', rule)
AST.add_filter('init', AST_init)

def ast_apply(block, item):
        if item.lex:
                return AST_item(item)
        if item.char in block.rules:
                return block.rules[item.char](block, item)
        else:
                return ast_apply(block, item.children[0])

def AST_set_time(block, t):
        block.t = t
        block.items = []
        if len(block.previous_block.items):
                block.ast = ast_apply(block, block.previous_block.items[0])
                if len(block.ast.children): # No AST elements
                        yac_walk(block, block.ast, 0, 0, 0, False, True)
        block.next_block.call('set_time', -1)
AST.add_filter('set_time', AST_set_time)

def AST_update_rule(block, rule):
        block.rules[rule[0]] = rule[1]
AST.add_filter('update_ast', AST_update_rule)

def ast_value(block, item):
        if item.children[0].lex:
                return AST_item(item, 'Value', [AST_item(item.children[0])])
        else:
                return ast_apply(block, item.children[0])

def ast_variable(block, item):
        return AST_item(item, 'Variable', [AST_item(item.children[0])])

def ast_unary(block, item):
        if len(item.children) == 2:
                node = ast_apply(block, item.children[1])
                if item.children[0].value == '-':
                        return AST_item(item.children[0], None, [node])
                else:
                        return node
        if len(item.children) == 3:
                return AST_item(item.children[1], None,
                                 [ast_apply(block, item.children[0]),
                                  ast_apply(block, item.children[2])])
        bug

def ast_unary_operation(block, item):
        if len(item.children) == 2:
                return [AST_item(item.children[0]),
                        ast_apply(block, item.children[1])]
        else:
                operation, tree = ast_unary_operation(block, item.children[0])
                return [operation, AST_item(item.children[1], None,
                        [tree, ast_apply(block, item.children[2])])]

def ast_binary(block, item):
        if len(item.children) == 3:
                return AST_item(item.children[1], None,
                                [ast_apply(block, item.children[0]),
                                 ast_apply(block, item.children[2])])
        else:
                operation, tree = ast_unary_operation(block, item.children[1])
                operation.children = [ast_apply(block, item.children[0]), tree]
                return operation

def ast_affectation(block, item):
        item = AST_item(item.children[0].children[-1], '=',
                [AST_item(item.children[0].children[0]),
                 ast_apply(block, item.children[1])])
        return item

def ast_program(block, item):
        return AST_item(item, 'Statement', [ast_apply(block, child)
                                            for child in item.children])

def ast_group(block, item):
        return ast_apply(block, item.children[1])

def ast_nice(item):
        if len(item.children) == 0:
                return item.value
        s = '[' + item.value
        for child in item.children:
                s += ',' + ast_nice(child)
        s += ']'
        return s

def AST_regtest(ast, dummy):
        for input, output in [
['a=1'          , "[Statement,[=,a,[Value,1]]]"],
['a=+1'         , "[Statement,[=,a,[Value,1]]]"],
['a=-1'         , "[Statement,[=,a,[-,[Value,1]]]]"],
['a=1+2'        , "[Statement,[=,a,[+,[Value,1],[Value,2]]]]"],
['a=1+2*3'      , "[Statement,[=,a,[+,[Value,1],[*,[Value,2],[Value,3]]]]]"],
['a=++1'        , "[Statement,[=,a,[Value,1]]]"],
['a=1++2'       , "[Statement,[=,a,[+,[Value,1],[Value,2]]]]"],
['a=1+2+3'      , "[Statement,[=,a,[+,[+,[Value,1],[Value,2]],[Value,3]]]]"],
['a=1+2+3+4'    , "[Statement,[=,a,[+,[+,[+,[Value,1],[Value,2]],[Value,3]],[Value,4]]]]"],
['a=2*+3+4'     , "[Statement,[=,a,[+,[*,[Value,2],[Value,3]],[Value,4]]]]"],
['a=2*+3/4'     , "[Statement,[=,a,[/,[*,[Value,2],[Value,3]],[Value,4]]]]"],
['a=1*2+3*4'    , "[Statement,[=,a,[+,[*,[Value,1],[Value,2]],[*,[Value,3],[Value,4]]]]]"],
['a=+1*+2++3*+4', "[Statement,[=,a,[+,[*,[Value,1],[Value,2]],[*,[Value,3],[Value,4]]]]]"],
['a=-(1)'       , "[Statement,[=,a,[-,[Value,1]]]]"],
['a=(1+2)*(3+4)', "[Statement,[=,a,[*,[+,[Value,1],[Value,2]],[+,[Value,3],[Value,4]]]]]"],
[' a = 5 ', '[Statement,[=,a,[Value,5]]]'],
[' a = ( 1 * 3 ) + 5 ', '[Statement,[=,a,[+,[*,[Value,1],[Value,3]],[Value,5]]]]'],
['a=1+2/+3', '[Statement,[=,a,[+,[Value,1],[/,[Value,2],[Value,3]]]]]'],
        ]:
                SRC.call('set', input)
                nice = ast_nice(ast.ast)
                if nice != output:
                        print("input:", input)
                        print("expected:", output)
                        print("computed:", nice)
                        YAC.call('dump')
                        print(yac_nice(YAC.items[0]))
                        bug
AST.add_filter('regtest', AST_regtest)

