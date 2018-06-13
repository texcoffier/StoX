class _OPT_(Block):
        title = "Code optimizer"
        name = "OPT"
        fullline_highlight = True
        time_travel = ['F9', 'F10']
OPT = blocks.append(_OPT_())

OPT.add_filter('dump', LEX_dump)
OPT.add_filter('html_init', canvas_html_init)
OPT.add_filter('html_draw', SRC_html_draw)

def OPT_init(block, dummy):
        block.rules = []
        block.call('update_opt', OPT_double_minus)
        block.call('update_opt', OPT_statement_merge)
OPT.add_filter('init', OPT_init)

def OPT_update_rule(block, rule):
        block.rules.append(rule)
OPT.add_filter('update_opt', OPT_update_rule)

def OPT_double_minus(item):
        if (item.rule == 'minus' and len(item.children) == 1
            and item.children[0].rule == 'minus'
            and len(item.children[0].children) == 1):
                return item.children[0].children[0]

def OPT_statement_merge(item):
        if (item.rule == 'Statement' and len(item.children) == 2
            and item.children[0].rule == 'Statement'
            and item.children[1].rule == 'Statement'
                ):
                children = []
                for child in item.children[0].children:
                        children.append(child)
                for child in item.children[1].children:
                        children.append(child)
                item.children = children
                return item

def OPT_walk(item):
        new_item = item.clone()
        for child in item.children:
                new_item.children.append(OPT_walk(child))
        for i, rule in enumerate(OPT.rules):
                if i >= OPT.t:
                        break
                new_item = rule(new_item) or new_item
        return new_item

def OPT_set_time(block, t):
        if t < 0:
                t = len(block.rules)
        block.t = t
        block.items = []
        if len(block.previous_block.items):
                root = OPT_walk(block.previous_block.items[0])
                y = yac_walk(block, root, 0, 0, 0, False, True)
                if t != len(block.rules):
                        block.append(Item('Rule:', 0, y+1))
                        block.append(Item(block.rules[t].name, 0, y+2))
        block.next_block.set_time(0)
OPT.add_filter('set_time', OPT_set_time)

OPT_key_codes = {'F9': -1, 'F10': +1}
def OPT_key(blocks, event):
        if event.key in OPT_key_codes:
                OPT.set_time(min(max(0, OPT.t + OPT_key_codes[event.key]),
                                     len(OPT.rules)))
                stop_event(event)
blocks.add_filter('key', OPT_key)
