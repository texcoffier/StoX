def font_size_key(blocks, event):
        if event.ctrlKey:
                change = 0
                if event.key == '+':
                        change = 1.1
                elif event.key == '-':
                        change = 0.9
                if change:
                        for block in blocks.blocks:
                                block.fontsize *= change
                        stop_event(event)
blocks.add_filter('key', font_size_key)

