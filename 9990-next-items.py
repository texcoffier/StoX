
def compute_next_items(block, t):
        for item in block.items:
                for i in item.previous_items:
                        i.next_items = []
        for item in block.items:
                for i in item.previous_items:
                        i.next_items.append(item)

for block in blocks.blocks:
        block.add_filter('set_time', compute_next_items)

