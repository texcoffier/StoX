"""Core: main program. Starts JavaScript event handles"""

if body:
        def keyevent(event):
                event = event or window.event
                blocks.call('key', event)
                blocks.call('html_draw')
        def keyup(event):
                event = event or window.event
                blocks.call('keyup', event)
        def drawevent():
                blocks.call('html_draw')
                SRC.cursor_visible = 1 - SRC.cursor_visible
        def mousemoveevent(event):
                blocks.call('mousemove', event)
        def mousedownevent(event):
                blocks.call('mousedown', event)
        def mousewheelevent(event):
                blocks.call('mousewheel', event)

        blocks.call('html_init', body)
        setInterval(drawevent, 400)
        window.addEventListener('keydown'       , keyevent       , False)
        window.addEventListener('keyup'         , keyup          , False)
        window.addEventListener('mousemove'     , mousemoveevent , False)
        window.addEventListener('mousedown'     , mousedownevent , False)
        window.addEventListener('DOMMouseScroll', mousewheelevent, False)
else:
        blocks.call('regtest')
        blocks.call('dump')
        
