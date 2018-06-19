"""Core utility: label/jump assembly and code generation"""

def context_jump_new_label(text):
        if text not in ASM.jump_labels_counters:
                ASM.jump_labels_counters[text] = 0
        label = text + '_' + str(ASM.jump_labels_counters[text])
        ASM.jump_labels_counters[text] += 1
        return label

def context_jump_add_label(from_item, label):
        item = from_item.clone()
        item.char = '   ' + label + ':'
        item.value = label
        item.y = len(ASM.items)
        item.instruction = None
        ASM.jump_labels[label] = ASM.segment_code
        ASM.append(item)

def context_jump_add_jump(item, label, test=None):
        if test is None:
                test = 'JUMP'
                feedback = None
        else:
                test = 'JUMP ' + test + '0'
                feedback = asm_feedback_pop
        asm_Item(ASM, item, test, label, asm_bytes(0xFFFF), feedback)
        ASM.jump_to_patch[ASM.segment_code - 2] = label

def context_jump_init(block, dummy):
        block.jump_labels = {} # LabelName => Addr or None
        block.jump_labels_counters = {}
        block.jump_to_patch = {} # Addr => LabelName
        block.new_label = context_jump_new_label
        block.add_label = context_jump_add_label
        block.add_jump  = context_jump_add_jump

def context_jump_done(block, dummy):
        for addr in block.jump_to_patch:
                label = block.jump_to_patch[addr]
                block.cpu.set_data_word(int(addr), block.jump_labels[label])

ASM.add_filter('set_time', context_jump_init, True)
ASM.add_filter('set_time', context_jump_done)

