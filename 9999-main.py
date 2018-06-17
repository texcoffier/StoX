#!/usr/bin/python3

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
        blocks.call('final_init')
        setInterval(drawevent, 400)
        window.addEventListener('keydown'  , keyevent      , False)
        window.addEventListener('mousemove', mousemoveevent, False)
        window.addEventListener('mousedown', mousedownevent, False)
else:
        blocks.call('regtest')
        blocks.dump()
        
