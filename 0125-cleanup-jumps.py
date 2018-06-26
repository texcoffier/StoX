"""Optimize: remove jumps to the next instruction"""

def cleanup_jumps(block, item):
        if item.char[-1] != ':':
                return # Not a label
        if len(block.items) == 1:
                return # Nothing before the label
        before = block.items[-2]
        if before.instruction.stox_name[:4] != 'JUMP':
                return # The instruction before is not a JUMP
        if before.more != item.value:
                return # Not the same label
        if before.instruction.stox_name != 'JUMP':
                # Conditional jump to the next instruction!
                before.error = True
                return
        block.call('remove', before)
        del block.jump_to_patch[ASM.segment_code - 2]
        block.segment_code -= 3
        block.jump_labels[item.value] -= 3
ASM.add_filter('append', cleanup_jumps)
