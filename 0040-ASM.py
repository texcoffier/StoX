class _ASM_(Block):
        title = "Assembly language"
        name = "ASM"
        def declare(self, item, variable):
                if variable not in self.variables:
                        self.segment_heap -= 1
                        self.variables[variable] = self.segment_heap
                        asm_Item(self, item, '.heap # keep 2 bytes for «'
                                 + variable + '»')
                        self.cpu.memory[self.segment_heap] = item.clone().set_byte(0)
                else:
                        self.cpu.memory[self.variables[variable]].previous_items.append(item)
                return self.variables[variable]
        def add_code(self, item):
                self.cpu.memory[self.segment_code] = item
                item.addr = self.segment_code
                self.segment_code += 1
                item.asm = self.items[-1]
        def dump_cpu_and_memory(self):
                print('<register>')
                print('\tPC', self.cpu.PC.long())
                print('\tSP', self.cpu.SP.long())
                print('<register>')
                print('<memory>')
                for i in range(0, self.segment_code):
                        print('\t', i, self.cpu.memory[i].long())
                for i in range(self.segment_heap, self.segment_stack):
                        print('\t', i, self.cpu.memory[i].long())
                print('</memory>')
        def new_instruction(self, fct):
                self.call('new_instruction', fct)
ASM = blocks.append(_ASM_())

ASM.add_filter('dump', LEX_dump)
ASM.add_filter('html_init', canvas_html_init)
ASM.add_filter('html_draw', SRC_html_draw)

def ASM_new_instruction(block, fct):
        if hasattr(fct, 'stox_code'):
                if fct.stox_code in block.cpu.by_code:
                        alert('code yet used:', fct.stox_code)
        else:
                fct.stox_code = len(block.cpu.by_code)
                while fct.stox_code in block.cpu.by_code:
                        fct.stox_code += 1
        if not hasattr(fct, 'stox_name'):
                fct.stox_name = fct.__name__ or fct.name
        if not hasattr(fct, 'stox_size'):
                fct.stox_size = 0
        fct.stox_block = block
        block.cpu.by_code[fct.stox_code] = fct
        block.cpu.by_name[fct.stox_name] = fct
ASM.add_filter('new_instruction', ASM_new_instruction)

class CPU_emulator:
        def __init__(self):
                self.PC = Item('')
                self.SP = Item('')
                self.by_code = {}
                self.by_name = {}
                self.memory = {}
                self.reset()
        def reset(self):
                self.SP.set_word(0x8000)
                self.set_PC(0)
                i = 0x8000
                while i in self.memory:
                        self.memory[i].color = "#DDD"
                        i += 1

        def set_PC(self, value):
                self.PC.set_word(value)
                if self.PC.value in self.memory:
                        code = self.memory[self.PC.value]
                        self.PC.color = code.color
                        instruction = self.by_code[code.value]
                        self.PC.char += " " + instruction.stox_name
        def step(self):
                PC = self.PC.value
                if PC not in self.memory:
                        return False
                instruction = self.by_code[self.memory[PC].value]
                instruction(self)
                if self.PC.value == PC: # Not a JUMP
                        self.set_PC(PC + instruction.stox_size + 1)
                return True
        def run(self, max_steps=1<<30):
                while self.step() and max_steps:
                        max_steps -= 1
        def get_data_word(self):
                return (self.memory[self.PC.value+1].unsigned_value * 256
                      + self.memory[self.PC.value+2].unsigned_value)
        def get_data_byte(self):
                return self.memory[self.PC.value+1].value
        def set_data_word(self, address, value):
                self.memory[address].set_byte(clamp(value >> 8))
                self.memory[address+1].set_byte(clamp(value & 0xFF))
        def stack_push(self, value):
                self.memory[self.SP.value].set_byte(value)
                self.memory[self.SP.value].color = "#000"
                self.SP.set_word(self.SP.value + 1)
        def stack_pop(self):
                self.SP.set_word(self.SP.value - 1)
                self.memory[self.SP.value].color = "#DDD"
                return self.memory[self.SP.value].value
        def store_at(self, value):
                self.memory[value].set_byte(self.stack_pop())
        def load_at(self, value):
                try:
                        self.stack_push(self.memory[value].value)
                except:
                        self.stack_push(0xFFFF)
                        self.memory[self.SP.value-1].error = True

def ASM_init(block, dummy):
        block.rules = {}
        block.cpu = CPU_emulator()
        for rule in [
                ['Statement', asm_program],
                ['='        , asm_affectation],
                ['Value'    , asm_value],
                ['Variable' , asm_variable],
                ["+"        , asm_addition],
                ["-"        , asm_subtraction],
                ["*"        , asm_multiply],
                ["/"        , asm_divide],
                ]:
                ASM.call('update_asm', rule)

        def LOAD_IMMEDIATE(cpu):
                cpu.stack_push(cpu.get_data_byte())
        LOAD_IMMEDIATE.stox_size = 1
        def STORE_AT_ADDRESS(cpu):
                cpu.store_at(cpu.get_data_word())
        STORE_AT_ADDRESS.stox_size = 2
        def LOAD_AT_ADDRESS(cpu):
                cpu.load_at(cpu.get_data_word())
        LOAD_AT_ADDRESS.stox_size = 2
        def ADDITION(cpu):
                cpu.stack_push(cpu.stack_pop() + cpu.stack_pop())
        def SUBTRACTION(cpu):
                a = cpu.stack_pop()
                b = cpu.stack_pop()
                cpu.stack_push(b - a)
        def MULTIPLY(cpu):
                cpu.stack_push(cpu.stack_pop() * cpu.stack_pop())
        def DIVIDE(cpu):
                a = cpu.stack_pop()
                b = cpu.stack_pop()
                cpu.stack_push(b // a)
        def NEGATE(cpu): cpu.stack_push(-cpu.stack_pop())

        for fct in [LOAD_IMMEDIATE, STORE_AT_ADDRESS, LOAD_AT_ADDRESS,
                    ADDITION, SUBTRACTION, MULTIPLY, DIVIDE, NEGATE]:
                block.new_instruction(fct)

ASM.add_filter('init', ASM_init)

def asm_generate(block, item, data=None):
        if item.char in block.rules:
                return block.rules[item.char](block, item, data)

def ASM_update_rule(block, rule):
        block.rules[rule[0]] = rule[1]
ASM.add_filter('update_asm', ASM_update_rule)


def ASM_set_time(block, t):
        block.t = t
        block.cpu.reset()
        block.cpu.memory = {}
        block.variables = {}
        block.labels = {}
        block.segment_heap = 0x8000
        block.segment_code = 0x0000
        block.segment_stack = 0x8020
        for i in range(block.segment_heap, block.segment_stack):
                block.cpu.memory[i] = Item('', 3*(i%4)).set_byte(0x00)
        block.items = []
        if len(block.previous_block.items):
                asm_generate(block, block.previous_block.items[0])
                # Add arrows
                labels_addr = {}
                for item in block.items:
                        if item.char and item.char[-1] == ':':
                                labels_addr[item.value] = item.index
                for item in block.items:
                        if (item.instruction
                            and item.instruction.stox_name[:4] == 'JUMP'):
                                item.arrow_to = labels_addr[item.more]
        block.next_block.set_time(0)
ASM.add_filter('set_time', ASM_set_time)

def asm_past_feedback(item):
        item.rectangle()
        for i in item.previous_items:
                asm_past_feedback(i)

def asm_enhanced_feedback(asm):
        asm_past_feedback(asm)
        asm.code.rectangle()
        for i in range(asm.instruction.size):
                asm.block.cpu.memory[asm.code.addr + i + 1].rectangle()
        if asm.more_feedback:
                asm.more_feedback(asm)
        if asm.arrow_to:
                asm.block.ctx.strokeStyle = "#0F0"
                asm.draw_arrow()

def asm_feedback_push(asm):
        asm.block.cpu.memory[asm.block.cpu.SP.value].rectangle("#F00")

def asm_feedback_pop(asm):
        asm.block.cpu.memory[asm.block.cpu.SP.value-1].rectangle("#0F0")

def asm_Item(block, from_item, name, value='', codes=[], feedback=None):
        item = from_item.clone()
        item.char = '    ' + name + ' ' + value
        item.more = value
        item.y = len(block.items)
        block.append(item)
        if name not in block.cpu.by_name:
                item.instruction = None
                return
        instruction = block.cpu.by_name[name]
        if instruction.stox_size != len(codes):
                print(name, value, instruction.stox_name,
                      instruction.stox_size, codes)
                bug
        item.feedback = asm_enhanced_feedback
        item.more_feedback = feedback
        item.code = item.clone().set_byte(instruction.stox_code)
        item.instruction = instruction
        block.add_code(item.code)
        for code in codes:
                block.add_code(item.clone().set_byte(code))

def asm_program(block, item, data):
        for child in item.children:
                asm_generate(block, child)

def asm_bytes(value):
        return [clamp(int(value) >> 8), clamp(int(value) & 0xFF)]

def asm_affectation(block, item, data):
        asm_generate(block, item.children[1])
        variable_name = item.children[0].value
        addr = block.declare(item.children[0], variable_name)
        def feedback(asm):
                asm.block.cpu.memory[addr].rectangle("#F00")
                asm_feedback_pop(asm)
        asm_Item(block, item, 'STORE_AT_ADDRESS', variable_name,
                 asm_bytes(addr), feedback)

def asm_value(block, item, data):
        value = item.children[0].value
        asm_Item(block, item.children[0], 'LOAD_IMMEDIATE', value,
                 [int(value)], asm_feedback_push)

def asm_feedback_variable(asm):
        if asm.addr in asm.block.cpu.memory:
                asm.block.cpu.memory[asm.addr].rectangle("#0F0")
        asm_feedback_push(asm)

def asm_variable(block, item, data):
        variable_name = item.children[0].value
        if variable_name in block.variables:
                addr = block.variables[variable_name]
                block.cpu.memory[addr].previous_items.append(item.children[0])
        else:
                addr = 0xFFFF
        asm_Item(block, item.children[0], 'LOAD_AT_ADDRESS', variable_name,
                 asm_bytes(addr), asm_feedback_variable)
        block.items[-1].addr = addr
        if addr == 0xFFFF:
                block.items[-1].error = True


def asm_feedback_binary(asm):
        asm.block.cpu.memory[asm.block.cpu.SP.value-2].rectangle("#F80")
        asm.block.cpu.memory[asm.block.cpu.SP.value-1].rectangle("#0F0")

def asm_feedback_unary(asm):
        asm.block.cpu.memory[asm.block.cpu.SP.value-1].rectangle("#F80")

def asm_addition(block, item, data):
        asm_generate(block, item.children[0])
        asm_generate(block, item.children[1])
        asm_Item(block, item, 'ADDITION', '', [], asm_feedback_binary)

def asm_subtraction(block, item, data):
        if len(item.children) == 1:
                asm_generate(block, item.children[0])
                asm_Item(block, item, 'NEGATE', '', [], asm_feedback_unary)
        else:
                asm_generate(block, item.children[0])
                asm_generate(block, item.children[1])
                asm_Item(block, item, 'SUBTRACTION', '', [], asm_feedback_binary)

def asm_multiply(block, item, data):
        asm_generate(block, item.children[0])
        asm_generate(block, item.children[1])
        asm_Item(block, item, 'MULTIPLY', '', [], asm_feedback_binary)

def asm_divide(block, item, data):
        asm_generate(block, item.children[0])
        asm_generate(block, item.children[1])
        asm_Item(block, item, 'DIVIDE', '', [], asm_feedback_binary)

def ASM_dump(block, dummy_arg):
        block.dump_cpu_and_memory()
ASM.add_filter('dump', ASM_dump)

def ASM_regtest(block, dummy):
        SRC.call('set', 'a=1')
        m = block.cpu.memory[0]
        for input, char, value in [
                [-257, "FF",   -1],
                [-256, "00",   -0],
                [-129, "7F",  127],
                [-128, "80", -128],
                [  -1, "FF",   -1],
                [   0, "00",    0],
                [ 127, "7F",  127],
                [ 128, "80", -128],
                [ 129, "81", -127],
                [ 255, "FF",   -1],
                [ 256, "00",    0],
                [ 257, "01",    1],
        ]:
                m.set_byte(input)
                if m.char != char or m.value != value:
                        print("set_byte", input, "=>", m.char, m.value)
                        bug_set_byte
ASM.add_filter('regtest', ASM_regtest)

