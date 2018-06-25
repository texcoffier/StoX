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
