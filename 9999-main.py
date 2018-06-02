#!/usr/bin/python3

# 1+2/(+3)

blocks.init()

body = None

for block in blocks.blocks:
        print('Regression tests for «', block.title, "»")
        block.call('regtest')
        print("OK")

try:
        body = document.getElementsByTagName('BODY')[0]
except:
        pass

if body:
        def keyevent(event):
                event = event or window.event
                blocks.key(event)
                blocks.html_draw()
        def drawevent():
                blocks.html_draw()
                src = blocks.get('SRC')
                src.cursor_visible = 1 - src.cursor_visible

        blocks.get('SRC').call('set', 'a=1\nb=3\nc = (a+-+-b)/+2')
        blocks.html_init(body)
        setInterval(drawevent, 400)
        window.addEventListener('keypress', keyevent, False)
else:
        blocks.dump()
        
