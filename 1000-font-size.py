"""GUI: the font size chooser («Ctrl +» and «Ctrl -») or «Ctrl + mouse wheel»"""

def update_font_size(element, change):
        for block in blocks.blocks:
                if block.element is element:
                        if change == '+':
                                change = 1.1
                        else:
                                change = 0.9
                        block.call('fontsize',
                                float((block.fontsize * change).toFixed(1)))
                        break

def font_size_key(blocks, event):
        if event.ctrlKey:
                if event.key == '+' or event.key == '-':
                        update_font_size(event.target, event.key)
                        stop_event(event)
blocks.add_filter('key', font_size_key)

def font_size_mouse_wheel(blocks, event):
        if not event.ctrlKey:
                return
        if event.deltaY > 0:
                update_font_size(event.target, '-')
        else:
                update_font_size(event.target, '+')
        stop_event(event)
blocks.add_filter('mousewheel', font_size_mouse_wheel)

def help_zoom(block, help_window):
        help_window['top'] += '<p>Use «Control mouse wheel»  or «Control +» or «Control -» to zoom.'
blocks.add_filter('update_help', help_zoom)
