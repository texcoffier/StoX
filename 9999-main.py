#!/usr/bin/python3



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
                SRC.cursor_visible = 1 - SRC.cursor_visible
        def mousemoveevent(event):
                blocks.call('mousemove', event)
        def mousedownevent(event):
                blocks.call('mousedown', event)

        blocks.html_init(body)
        SRC.call('set', 'a=65\nwhile(a != 70)\n {\n  put(a)\n  a = a + 1\n }')
        blocks.call('final_init')
        setInterval(drawevent, 400)
        window.addEventListener('keydown'  , keyevent      , False)
        window.addEventListener('mousemove', mousemoveevent, False)
        window.addEventListener('mousedown', mousedownevent, False)
else:
        blocks.dump()
        
