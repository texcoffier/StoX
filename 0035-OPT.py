class OPT(Block):
        title = "Code optimizer"
        name = "OPT"
blocks.append(OPT())

blocks.get('OPT').add_filter('dump', LEX_dump)
blocks.get('OPT').add_filter('html_init', canvas_html_init)
blocks.get('OPT').add_filter('html_draw', SRC_html_draw)

def OPT_walk(block, old_item):
        # Remove double negation
        if (old_item.rule == 'minus'
                and len(old_item.children) == 1
                and old_item.children[0].rule == 'minus'
                and len(old_item.children[0].children) == 1):
                return OPT_walk(block, old_item.children[0].children[0])
        item = old_item.clone()
        for child in old_item.children:
                item.children.append(OPT_walk(block, child))
        return item

def OPT_set_time(block, t):
        block.t = t
        root = OPT_walk(block, block.previous_block.items[0])
        block.items = []
        yac_walk(block, root, 0, 0, 0, False, True)
        block.next_block.set_time(0)

blocks.get('OPT').add_filter('set_time', OPT_set_time)