"""GUI: autofocus on the block under the mouse (for text zooming)"""

def blocks_autofocus(blocks, event):
        for block in blocks.blocks:
                if block.element is event.target:
                        block.element.focus()
                        window.scrollTo(0, 0)
blocks.add_filter('mousemove', blocks_autofocus)
