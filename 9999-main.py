#!/usr/bin/python3

blocks.init()

for block in blocks.blocks:
        print('Regression tests for «', block.title, "»")
        block.call('regtest')
        print("OK")


if body:
        def keyevent(event):
                event = event or window.event
                blocks.key(event)
                blocks.html_draw()
        def drawevent():
                blocks.html_draw()
                src = blocks.get('SRC')
                src.cursor_visible = 1 - src.cursor_visible

        blocks.html_init(body)
        blocks.get('SRC').call('set', 'put(65)')
        setInterval(drawevent, 400)
        window.addEventListener('keypress', keyevent, False)
else:
        blocks.dump()
        
