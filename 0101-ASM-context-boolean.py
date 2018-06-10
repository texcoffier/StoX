
class BooleanContext:
        def __init__(self, label_true=None, label_false=None,
                     i_must_return_01=True):
                self.label_true         = label_true
                self.label_false        = label_false
                self.i_must_return_01   = i_must_return_01
                self.child_is_a_boolean = False
        def clone(self, label_true=None, label_false=None,
                  i_must_return_01=True):
                c = BooleanContext(label_true
                                        or self.label_true
                                        or ASM.new_label('bool_true'),
                                      label_false
                                        or self.label_false
                                        or ASM.new_label('bool_false'),
                                      i_must_return_01
                                      )
                if self.label_true or self.label_false:
                        c.i_must_return_01 = False
                return c
        def dump(self):
                print(self.label_true, self.label_false, self.i_must_return_01,
                      self.child_is_a_boolean)

class BooleanContextStack:
        def __init__(self):
                self.stack = [BooleanContext()]
        def begin(self, label_true=None, label_false=None, i_must_return_01=True):
                self.stack[-1].child_is_a_boolean = True
                self.stack.append(self.stack[-1].clone(label_true, label_false,
                                                       i_must_return_01))
        def jump_true(self, item, test=None):
                if not self.stack[-1].child_is_a_boolean:
                        ASM.add_jump(item, self.stack[-1].label_true, test)
        def jump_false(self, item, test=None):
                if not self.stack[-1].child_is_a_boolean:
                        ASM.add_jump(item, self.stack[-1].label_false, test)
        def add_label_true(self, item):
                ASM.add_label(item, self.stack[-1].label_true)
        def add_label_false(self, item):
                ASM.add_label(item, self.stack[-1].label_false)
        def end(self, item):
                if self.stack[-1].i_must_return_01:
                        self.add_label_true(item)
                        asm_Item(ASM, item, 'LOAD_IMMEDIATE', '1', [1],
                                 asm_feedback_push)
                        label_end = ASM.new_label('bool_end')
                        ASM.add_jump(item, label_end)

                        self.add_label_false(item)
                        asm_Item(ASM, item, 'LOAD_IMMEDIATE', '0', [0],
                                 asm_feedback_push)
                        ASM.add_label(item, label_end)
                self.stack.pop()

BCS = BooleanContextStack()



