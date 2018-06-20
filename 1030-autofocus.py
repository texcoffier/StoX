"""GUI: autofocus on the block under the mouse (for text zooming)"""

def blocks_autofocus(blocks, event):
        for block in blocks.blocks:
                if block.element is event.target:
                        block.element.focus()
blocks.add_filter('mousemove', blocks_autofocus)
