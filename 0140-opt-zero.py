"""Optimize: -0, x+0, 0+x, x-0, 0-x, 0*x, x*0"""

def is_zero(item):
        return item.rule == 'Value' and int(item.children[0].value) % 256 == 0

def OPT_minus_0(item):
        if (item.rule == 'minus' and len(item.children) == 1
            and is_zero(item.children[0])):
                    return item.children[0]
OPT.call('update_opt', OPT_minus_0)

def OPT_remove_add_0(item):
        if item.rule in ['plus', 'minus'] and len(item.children) == 2:
                if is_zero(item.children[1]):
                        return item.children[0]
                if is_zero(item.children[0]):
                        if item.rule == 'plus':
                                return item.children[1]
                        else:
                                item.children = [item.children[1]]
        return item
OPT.call('update_opt', OPT_remove_add_0)

def OPT_remove_multiply_0(item):
        if item.rule == 'star' and len(item.children) == 2:
                if is_zero(item.children[0]):
                        return item.children[0]
                if is_zero(item.children[1]):
                        return item.children[1]
        return item
OPT.call('update_opt', OPT_remove_multiply_0)

def zero_regtest(tty, dummy):
        for src, expect in [
                ['0+0+0+1+0+2+0+0+3', '[+,[+,[Value,1],[Value,2]],[Value,3]]'],
                ['0-7'             , '[-,[Value,7]]'],
                ['0-7-8'           , '[-,[-,[Value,7]],[Value,8]]'],
                ['0-7-0-8'         , '[-,[-,[Value,7]],[Value,8]]'],
                ['-0+0-7+0-0-8-0+0', '[-,[-,[Value,7]],[Value,8]]'],
                ['0*7+8*0'         , '[Value,0]'],
                ['-(0-7)'          , '[Value,7]'],
                ['256+7'           , '[Value,7]'],
                ]:
                SRC.call('set', src)
                if ast_nice(OPT.items[0]) != expect:
                        print('Computed:', ast_nice(OPT.items[0]))
                        print('Expected:', expect)
                        bug
TTY.add_filter('regtest', zero_regtest)
