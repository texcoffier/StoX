"""Core addon: the hook «remove»"""

def remove_item(block, item):
        for i in range(item.index, len(block.items) - 1):
                block.items[i] = block.items[i+1]
                block.items[i].index -= 1
                block.items[i].y -= 1
        block.items.pop()

for block in blocks.blocks:
        block.add_filter('remove', remove_item)
