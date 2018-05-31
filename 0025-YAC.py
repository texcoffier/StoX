class YAC(Block):
        title = "Syntaxique analyser"
        name = "YAC"
blocks.append(YAC())

blocks.get('YAC').add_filter('dump', LEX_dump)
blocks.get('YAC').add_filter('html_init', canvas_html_init)
blocks.get('YAC').add_filter('html_draw', SRC_html_draw)

def YAC_init(block, dummy):
        block.rules = []
        block.fontsize = 8
        block.line_spacing = 1
        s = ['separator', '*']
        for rule in [
           ['Variable='  , [['word'], s, ['affectation']]],
           ['Variable'   , [['word']]],
           ['Value'      , [['Variable']]],
           ['Value'      , [['number']]],
           ['Value'      , [['Group']]],
           ['Expression' , [['Value']]],
           ['Group'      , [['open'], s, ['Expression']  , s, ['close']]],
           ['Binary'     , [['Expression'], s, ['star']  , s, ['Unary']]],
           ['Binary'     , [['Expression'], s, ['slash'] , s, ['Unary']]],
           ['Unary'      , [['plus'], s, ['Expression']]],
           ['Unary'      , [['minus'], s, ['Expression']]],
           ['Unary'      , [['Unary']     , s, ['star']  , s, ['Expression']]],
           ['Unary'      , [['Unary']     , s, ['slash'] , s, ['Expression']]],
           ['Unary'      , [['Unary']     , s, ['star']  , s, ['Unary']]],
           ['Unary'      , [['Unary']     , s, ['slash'] , s, ['Unary']]],
           ['Binary'     , [['Expression'], s, ['star']  , s, ['Expression']]],
           ['Binary'     , [['Expression'], s, ['slash'] , s, ['Expression']]],
           ['Binary'     , [['Expression'], s, ['Unary']]],
           ['Expression' , [['Binary']]],
           ['Value'      , [['Unary']]],
           ['Affectation', [s, ['Variable='], s, ['Expression']]],
           ['Statement'  , [['Affectation']]],
           ['Program'    , [['Statement', '*']]],
        ]:
                block.call('update_rule', rule)
blocks.get('YAC').add_filter('init', YAC_init)

class Rule:
        def __init__(self, name, data):
                self.name = name
                self.lexems = []
                for x in data:
                        if len(x) == 1:
                                x = [x[0], '1']
                        self.lexems.append(x)
        def long(self):
                return self.name + ':' + self.lexems

def YAC_update_rule(block, rule):
        block.rules.append(Rule(rule[0], rule[1]))
blocks.get('YAC').add_filter('update_rule', YAC_update_rule)

def rule_match(items, position, rule):
        for name, repeat in rule.lexems:
                if position == len(items):
                        return False
                if repeat == '*':
                        while position < len(items) and name == items[position].rule:
                                position += 1
                else:
                        if name != items[position].rule:
                                return False
                        position += 1
        return position

def rule_apply(block, items, rule):
        """Returns the Item"""
        position = 0
        after = []
        while position < len(items):
                p = rule_match(items, position, rule)
                if p is False or position == p:
                        after.append(items[position])
                        position += 1
                        continue
                match = Item(rule.name)
                match.children = items[position:p]
                match.lex = False
                after.append(match)
                position = p
                while position < len(items):
                        after.append(items[position])
                        position += 1
                return after

def yac_walk(block, item, x, y, depth, bad, expand=False):
        item.x = x
        item.y = y
        if bad:
                item.error = True
        block.append(item)
        if not expand and len(item.children) == 1:
                child = item.children[0]
                x += len(item.char)
                y = yac_walk(block, child, x, y, depth, bad, expand)
        else:
                depth += 1
                x = 1.5 * depth
                y += 1
                if item.children:
                        for child in item.children:
                                y = yac_walk(block, child, x, y, depth, bad, expand)
        return y

def yac_nice(item):
        if len(item.children) == 0:
                return item.char
        if len(item.children) == 1:
                return yac_nice(item.children[0])
        if item.char == 'Unary' and len(item.children) == 2:
                return (item.children[0].char
                        + yac_nice(item.children[1]))
        s = '(' + item.char[0]
        for i in item.children:
                s += ' ' + yac_nice(i)
        return s + ')'

def YAC_set_time(block, t):
        block.t = t
        items = []
        for i in block.previous_block.items:
                item = i.clone()
                item.char = item.char.replace("\n", "\\n")
                item.lex = True
                items.append(item)
        change = True
        while change:
                change = False
                for rule in block.rules:
                        new_items = rule_apply(block, items, rule)
                        if new_items:
                                items = new_items
                                ###################
                                ###################
                                ###################
                                #print(' '.join(i.rule for i in items))
                                ###################
                                ###################
                                ###################
                                change = True
                                break
        block.items = []
        y = 0
        bad = False
        for root in items:
                y = yac_walk(block, root, 0, y, 0, bad)
                bad = True
        block.next_block.set_time(0)
blocks.get('YAC').add_filter('set_time', YAC_set_time)

def YAC_regtest(yac, dummy):
        for input, output in [
['a=1'          ,'(A (V a =) 1)'],
['a=+1'         ,'(A (V a =) +1)'],
['a=-1'         ,'(A (V a =) -1)'],
['a=1+2'        ,'(A (V a =) (B 1 +2))'],
['a=1+2*3'      ,'(A (V a =) (B 1 (U +2 * 3)))'],
['a=++1'        ,'(A (V a =) ++1)'],
['a=1++2'       , '(A (V a =) (B 1 ++2))'],
['a=1+2+3'      , '(A (V a =) (B (B 1 +2) +3))'],
['a=1+2+3+4'    , '(A (V a =) (B (B (B 1 +2) +3) +4))'],
['a=2*+3+4'     ,  '(A (V a =) (B (B 2 * +3) +4))'],
['a=2*+3/4'     ,  '(A (V a =) (B (B 2 * +3) / 4))'],
['a=1*2+3*4'    ,  '(A (V a =) (B (B 1 * 2) (U +3 * 4)))'],
['a=+1*+2++3*+4', '(A (V a =) (B (U +1 * +2) +(U +3 * +4)))'],
['a=-(1)'       , '(A (V a =) -(G ( 1 )))'],
['a=(1+2)*(3+4)', '(A (V a =) (B (G ( (B 1 +2) )) * (G ( (B 3 +4) ))))'],
        ]:
                blocks.get('SRC').call('set', input)
                nice = yac_nice(yac.items[0])
                if nice != output:
                        print("input:", input)
                        print("expected:", output)
                        print("computed:", nice)
                        bug
        print("test_yac OK")
blocks.get('YAC').add_filter('regtest', YAC_regtest)
