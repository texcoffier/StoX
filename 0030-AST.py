class AST(Block):
        title = "Abstract Syntax Tree"
        name = "AST"
        fullline_highlight = True
blocks.append(AST())

blocks.get('AST').add_filter('dump', LEX_dump)
blocks.get('AST').add_filter('html_init', canvas_html_init)
blocks.get('AST').add_filter('html_draw', SRC_html_draw)

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
                ['Unary', ast_unary],
                ['Variable', ast_variable],
                ['Binary', ast_binary],
                ['Value', ast_value],
                ['Group', ast_group],
                ['Program', ast_program],
                ]:
                blocks.get('AST').call('update_rule', rule)
blocks.get('AST').add_filter('init', AST_init)

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
                yac_walk(block, block.ast, 0, 0, 0, False, True)
        block.next_block.set_time(0)
blocks.get('AST').add_filter('set_time', AST_set_time)

def AST_update_rule(block, rule):
        block.rules[rule[0]] = rule[1]
blocks.get('AST').add_filter('update_rule', AST_update_rule)

def ast_children(item):
        return [i for i in item.children if i.rule != 'separator']

def ast_value(block, item):
        if item.children[0].lex:
                return AST_item(item, 'Value', [AST_item(item.children[0])])
        else:
                return ast_apply(block, item.children[0])

def ast_variable(block, item):
        return AST_item(item, 'Variable', [AST_item(item.children[0])])

def ast_unary(block, item):
        child = ast_children(item)
        if len(child) == 2:
                node = ast_apply(block, child[1])
                if child[0].value == '-':
                        return AST_item(child[0], None, [node])
                else:
                        return node
        if len(child) == 3:
                return AST_item(child[1], None,
                                 [ast_apply(block, child[0]),
                                  ast_apply(block, child[2])])
        bug

def ast_unary_operation(block, item):
        child = ast_children(item)
        if len(child) == 2:
                return [AST_item(child[0]), ast_apply(block, child[1])]
        else:
                operation, tree = ast_unary_operation(block, child[0])
                return [operation, AST_item(child[1], None,
                        [tree, ast_apply(block, child[2])])]

def ast_binary(block, item):
        child = ast_children(item)
        if len(child) == 3:
                return AST_item(child[1], None, [ast_apply(block, child[0]),
                                  ast_apply(block, child[2])])
        else:
                operation, tree = ast_unary_operation(block, child[1])
                operation.children = [ast_apply(block, child[0]), tree]
                return operation

def ast_affectation(block, item):
        child = ast_children(item)
        item = AST_item(child[0].children[-1], '=',
                [AST_item(child[0].children[0]), ast_apply(block, child[1])])
        #item.previous_items = child[0].children
        return item

def ast_program(block, item):
        t = []
        for child in ast_children(item):
                t.append(ast_apply(block, child))
        return AST_item(item, 'Program', t)

def ast_group(block, item):
        return ast_apply(block, ast_children(item)[1])

def ast_nice(item):
        if len(item.children) == 0:
                return item.char
        s = '[' + item.char
        for child in item.children:
                s += ',' + ast_nice(child)
        s += ']'
        return s

def AST_regtest(ast, dummy):
        for input, output in [
['a=1'          , "[Program,[=,a,[Value,1]]]"],
['a=+1'         , "[Program,[=,a,[Value,1]]]"],
['a=-1'         , "[Program,[=,a,[-,[Value,1]]]]"],
['a=1+2'        , "[Program,[=,a,[+,[Value,1],[Value,2]]]]"],
['a=1+2*3'      , "[Program,[=,a,[+,[Value,1],[*,[Value,2],[Value,3]]]]]"],
['a=++1'        , "[Program,[=,a,[Value,1]]]"],
['a=1++2'       , "[Program,[=,a,[+,[Value,1],[Value,2]]]]"],
['a=1+2+3'      , "[Program,[=,a,[+,[+,[Value,1],[Value,2]],[Value,3]]]]"],
['a=1+2+3+4'    , "[Program,[=,a,[+,[+,[+,[Value,1],[Value,2]],[Value,3]],[Value,4]]]]"],
['a=2*+3+4'     , "[Program,[=,a,[+,[*,[Value,2],[Value,3]],[Value,4]]]]"],
['a=2*+3/4'     , "[Program,[=,a,[/,[*,[Value,2],[Value,3]],[Value,4]]]]"],
['a=1*2+3*4'    , "[Program,[=,a,[+,[*,[Value,1],[Value,2]],[*,[Value,3],[Value,4]]]]]"],
['a=+1*+2++3*+4', "[Program,[=,a,[+,[*,[Value,1],[Value,2]],[*,[Value,3],[Value,4]]]]]"],
['a=-(1)'       , "[Program,[=,a,[-,[Value,1]]]]"],
['a=(1+2)*(3+4)', "[Program,[=,a,[*,[+,[Value,1],[Value,2]],[+,[Value,3],[Value,4]]]]]"],
[' a = 5 ', '[Program,[=,a,[Value,5]]]'],
[' a = ( 1 * 3 ) + 5 ', '[Program,[=,a,[+,[*,[Value,1],[Value,3]],[Value,5]]]]'],
['a=1+2/+3', '[Program,[=,a,[+,[Value,1],[/,[Value,2],[Value,3]]]]]'],
        ]:
                blocks.get('SRC').call('set', input)
                nice = ast_nice(ast.ast)
                if nice != output:
                        print("input:", input)
                        print("expected:", output)
                        print("computed:", nice)
                        blocks.get('YAC').dump()
                        print(yac_nice(blocks.get('YAC').items[0]))
                        bug
blocks.get('AST').add_filter('regtest', AST_regtest)

