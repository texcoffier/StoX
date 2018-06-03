#!/usr/bin/python3

# backspace on last char

blocks.init()

# blocks.get('SRC').call('set', '+')

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

        blocks.html_init(body)
        blocks.get('SRC').call('set', 'a=1\nb=3\nc = (a+-+-b)/+2')
        setInterval(drawevent, 400)
        window.addEventListener('keypress', keyevent, False)
else:
        blocks.dump()
        
