"""GUI: the font size chooser («Ctrl +» and «Ctrl -»)"""

def font_size_key(blocks, event):
        if event.ctrlKey:
                change = 0
                if event.key == '+':
                        change = 1.1
                elif event.key == '-':
                        change = 0.9
                if change:
                        for block in blocks.blocks:
                                if block.element is event.target:
                                        block.call('fontsize',
                                                   float((block.fontsize * change).toFixed(1)))
                        stop_event(event)
blocks.add_filter('key', font_size_key)

def set_fontsize(block, size):
        block.fontsize = size
for block in blocks.blocks:
        block.add_filter('fontsize', set_fontsize)
