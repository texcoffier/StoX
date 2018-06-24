"""Core: Block management"""

blocks = Blocks()

def blocks_dump(blocks, dummy_arg):
        print('<dump>')
        for block in blocks.blocks:
                print('\t<', block.name, 't=', block.t, '>')
                block.call('dump')
                print('\t</', block.name, '>')
        print('</dump>')
blocks.add_filter('dump', blocks_dump)


def set_fontsize(block, size):
        block.fontsize = size
        block.update_font_size()
        if block.i_want_minimal_height:
                block.set_to_minimal_height()

def blocks_init(blocks, dummy_arg):
        blocks.nr_columns = 0
        for block in blocks.blocks:
                block.add_filter('fontsize', set_fontsize)
                if block.window_top:
                        blocks.nr_columns += 1
                block.call('init', dummy_arg)
blocks.add_filter('init', blocks_init)

def blocks_html_init(blocks, body):
        blocks.element = document.createElement('DIV')
        blocks.element.style.overflow = 'hidden'
        body.appendChild(blocks.element)
        for block in blocks.blocks:
                block.call('html_init', block.title)
                block.call('fontsize', block.fontsize)
blocks.add_filter('html_init', blocks_html_init)

def blocks_html_draw(blocks, body):
        for block in blocks.blocks:
                block.call('html_draw')
                block.call('draw_cursor')
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

def blocks_regtest(blocks, dummy):
        for block in blocks.blocks:
                print('Regression tests for «', block.title, "»")
                block.call('regtest')
                print("OK")
blocks.add_filter('regtest', blocks_regtest)

translate_keys = {'PageUp': '⇞', 'PageDown': '⇟', 'y': 'Y', 'z': 'Z'}

def blocks_history_key(blocks, event):
        if event.metaKey or event.altKey:
                return
        key = event.key
        if key in translate_keys:
                key = translate_keys[key]
        if event.ctrlKey:
                key = '^' + key
        for block in blocks.blocks:
                if not block.time_travel:
                        continue
                if block.time_travel[0] == key:
                        block.time_travel_back()
                elif block.time_travel[1] == key:
                        block.time_travel_forward()
                else:
                        continue
                stop_event(event)
                return
blocks.add_filter('key', blocks_history_key)
