"""GUI: navigate in the history with the mouse wheel"""

def blocks_mouse_wheel(blocks, event):
        if event.metaKey or event.altKey or event.ctrlKey:
                return
        for block in blocks.blocks:
                if block.element is event.target:
                        if block.time_travel:
                                if event.deltaY < 0:
                                        block.time_travel_forward()
                                else:
                                        block.time_travel_back()
                        break
blocks.add_filter('mousewheel', blocks_mouse_wheel)

def help_mouse_wheel(block, help_window):
        help_window['top'] += '<p>Use the «mouse wheel» to travel in the time.'
blocks.add_filter('update_help', help_mouse_wheel)
