#!/usr/bin/python3

# 1+2/(+3)
# allocation variables
# génération code

blocks.init()

for block in blocks.blocks:
        print(block.title)
        block.call('regtest')

try:
        body = document.getElementsByTagName('BODY')[0]
except:
        body = None

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
        
