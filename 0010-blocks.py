blocks = Blocks()

def blocks_dump(blocks, dummy_arg):
        print('<dump>')
        for block in blocks.blocks:
                print('\t<', block.name, 't=', block.t, '>')
                block.dump(dummy_arg)
                print('\t</', block.name, '>')
        print('</dump>')
blocks.add_filter('dump', blocks_dump)

def blocks_init(blocks, dummy_arg):
        for block in blocks.blocks:
                block.init(dummy_arg)
blocks.add_filter('init', blocks_init)

def blocks_html_init(blocks, body):
        blocks.element = document.createElement('DIV')
        body.appendChild(blocks.element)
        for block in blocks.blocks:
                block.html_init(block.title)
blocks.add_filter('html_init', blocks_html_init)

def blocks_html_draw(blocks, body):
        for block in blocks.blocks:
                block.html_draw()
                block.draw_cursor()
blocks.add_filter('html_draw', blocks_html_draw)

def blocks_mousemove(blocks, event):
        selected = None
        for block in blocks.blocks:
                if block.element is event.target:
                        selected = block
                        break
        if selected is None:
                return
        x = event.x - selected.element.offsetLeft
        y = event.y - selected.element.offsetTop
        for item in selected.items:
                if item.contains(x, y):
                        blocks.call('highlight', item)
                        break
blocks.add_filter('mousemove', blocks_mousemove)

def hightlight_recursive(blocks, item, past):
        item.rectangle()
        if item.block is SRC:
                SRC.mousemove = item
        if past:
                items = item.previous_items
        else:
                items = item.next_items
        for p in items:
                hightlight_recursive(blocks, p, past)
def hightlight(blocks, item):
        hightlight_recursive(blocks, item, True)
        hightlight_recursive(blocks, item, False)
blocks.add_filter('highlight', hightlight)

