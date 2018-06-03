class ASM(Block):
        title = "Assembly language"
        name = "ASM"
        def declare(self, item, variable):
                if variable not in self.variables:
                        self.segment_heap -= 1
                        self.variables[variable] = self.segment_heap
                        asm_Item(self, item, '.HEAP # keep 2 bytes for «'
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
blocks.append(ASM())

blocks.get('ASM').add_filter('dump', LEX_dump)
blocks.get('ASM').add_filter('html_init', canvas_html_init)
blocks.get('ASM').add_filter('html_draw', SRC_html_draw)

class Instruction:
        def __init__(self, code, name, size, execute):
                self.code = code
                self.name = name
                self.size = size
                self.execute = execute
                self.block = blocks.get('ASM')
                self.block.cpu.by_code[code] = self
                self.block.cpu.by_name[name] = self

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
                        self.PC.char += " " + instruction.name
        def step(self):
                if self.PC.value not in self.memory:
                        return
                instruction = self.by_code[self.memory[self.PC.value].value]
                instruction.execute(self)
                self.set_PC(self.PC.value + instruction.size + 1)
        def get_data_word(self):
                return (self.memory[self.PC.value+1].unsigned_value * 256
                      + self.memory[self.PC.value+2].unsigned_value)
        def get_data_byte(self):
                return self.memory[self.PC.value+1].value
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
                ['Program' , asm_program],
                ['='       , asm_affectation],
                ['Value'   , asm_value],
                ['Variable', asm_variable],
                ["+"       , asm_addition],
                ["-"       , asm_subtraction],
                ["*"       , asm_multiply],
                ["/"       , asm_divide],
                ]:
                blocks.get('ASM').call('update_rule', rule)
        def x00(cpu): cpu.stack_push(cpu.get_data_byte())
        Instruction(0x00, "LOAD IMMEDIATE"  , 1, x00)
        def x01(cpu): cpu.store_at(cpu.get_data_word())
        Instruction(0x01, "STORE AT ADDRESS", 2, x01)
        def x02(cpu): cpu.load_at(cpu.get_data_word())
        Instruction(0x02, "LOAD AT ADDRESS" , 2, x02)
        def x03(cpu): cpu.stack_push(cpu.stack_pop() + cpu.stack_pop())
        Instruction(0x03, "ADDITION"        , 0, x03)
        def x04(cpu):
                a = cpu.stack_pop()
                b = cpu.stack_pop()
                cpu.stack_push(b - a)
        Instruction(0x04, "SUBTRACTION"     , 0, x04)
        def x05(cpu): cpu.stack_push(cpu.stack_pop() * cpu.stack_pop())
        Instruction(0x05, "MULTIPLY"        , 0, x05)
        def x06(cpu):
                a = cpu.stack_pop()
                b = cpu.stack_pop()
                cpu.stack_push(b // a)
        Instruction(0x06, "DIVIDE"          , 0, x06)
        def x07(cpu): cpu.stack_push(-cpu.stack_pop())
        Instruction(0x07, "NEGATE"          , 0, x07)

blocks.get('ASM').add_filter('init', ASM_init)

def asm_generate(block, item):
        if item.char in block.rules:
                block.rules[item.char](block, item)

def ASM_update_rule(block, rule):
        block.rules[rule[0]] = rule[1]
blocks.get('ASM').add_filter('update_rule', ASM_update_rule)

def ASM_set_time(block, t):
        block.t = t
        block.cpu.reset()
        block.cpu.memory = {}
        block.variables = {}
        block.segment_heap = 0x8000
        block.segment_code = 0x0000
        block.segment_stack = 0x8020
        for i in range(block.segment_heap, block.segment_stack):
                block.cpu.memory[i] = Item('', 3*(i%4)).set_byte(0x00)
        block.items = []
        if len(block.previous_block.items):
                asm_generate(block, block.previous_block.items[0])
        block.next_block.set_time(0)
blocks.get('ASM').add_filter('set_time', ASM_set_time)

def asm_enhanced_feedback(asm):
        asm.rectangle()
        asm.code.rectangle()
        for i in range(asm.instruction.size):
                asm.block.cpu.memory[asm.code.addr + i + 1].rectangle()
        if asm.more_feedback:
                asm.more_feedback(asm)

def asm_feedback_push(asm):
        asm.block.cpu.memory[asm.block.cpu.SP.value].rectangle("#F00")

def asm_feedback_pop(asm):
        asm.block.cpu.memory[asm.block.cpu.SP.value-1].rectangle("#0F0")

def asm_Item(block, from_item, name, value='', codes=[], feedback=None):
        item = from_item.clone()
        item.char = name + ' ' + value
        item.y = len(block.items)
        block.append(item)
        if name not in block.cpu.by_name:
                return
        instruction = block.cpu.by_name[name]
        if instruction.size != len(codes):
                bug
        item.feedback = asm_enhanced_feedback
        item.more_feedback = feedback
        item.code = item.clone().set_byte(instruction.code)
        item.instruction = instruction
        block.add_code(item.code)
        for code in codes:
                block.add_code(item.clone().set_byte(code))

def asm_program(block, item):
        for child in item.children:
                asm_generate(block, child)

def asm_bytes(value):
        return [clamp(int(value) >> 8), clamp(int(value) & 0xFF)]

def asm_affectation(block, item):
        asm_generate(block, item.children[1])
        variable_name = item.children[0].value
        addr = block.declare(item.children[0], variable_name)
        def feedback(asm):
                asm.block.cpu.memory[addr].rectangle("#F00")
                asm_feedback_pop(asm)
        asm_Item(block, item, 'STORE AT ADDRESS', variable_name,
                 asm_bytes(addr), feedback)

def asm_value(block, item):
        value = item.children[0].value
        asm_Item(block, item.children[0], 'LOAD IMMEDIATE', value,
                 [int(value)], asm_feedback_push)

def asm_feedback_variable(asm):
        if asm.addr in asm.block.cpu.memory:
                asm.block.cpu.memory[asm.addr].rectangle("#0F0")
        asm_feedback_push(asm)

def asm_variable(block, item):
        variable_name = item.children[0].value
        if variable_name in block.variables:
                addr = block.variables[variable_name]
                block.cpu.memory[addr].previous_items.append(item.children[0])
        else:
                addr = 0xFFFF
        asm_Item(block, item.children[0], 'LOAD AT ADDRESS', variable_name,
                 asm_bytes(addr), asm_feedback_variable)
        block.items[-1].addr = addr
        if addr == 0xFFFF:
                block.items[-1].error = True


def asm_feedback_binary(asm):
        asm.block.cpu.memory[asm.block.cpu.SP.value-2].rectangle("#F80")
        asm.block.cpu.memory[asm.block.cpu.SP.value-1].rectangle("#0F0")

def asm_feedback_unary(asm):
        asm.block.cpu.memory[asm.block.cpu.SP.value-1].rectangle("#F80")

def asm_addition(block, item):
        asm_generate(block, item.children[0])
        asm_generate(block, item.children[1])
        asm_Item(block, item, 'ADDITION', '', [], asm_feedback_binary)

def asm_subtraction(block, item):
        if len(item.children) == 1:
                asm_generate(block, item.children[0])
                asm_Item(block, item, 'NEGATE', '', [], asm_feedback_unary)
        else:
                asm_generate(block, item.children[0])
                asm_generate(block, item.children[1])
                asm_Item(block, item, 'SUBTRACTION', '', [], asm_feedback_binary)

def asm_multiply(block, item):
        asm_generate(block, item.children[0])
        asm_generate(block, item.children[1])
        asm_Item(block, item, 'MULTIPLY', '', [], asm_feedback_binary)

def asm_divide(block, item):
        asm_generate(block, item.children[0])
        asm_generate(block, item.children[1])
        asm_Item(block, item, 'DIVIDE', '', [], asm_feedback_binary)

def ASM_dump(block, dummy_arg):
        block.dump_cpu_and_memory()
blocks.get('ASM').add_filter('dump', ASM_dump)

def ASM_regtest(block, dummy):
        blocks.get('SRC').call('set', 'a=1')
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
blocks.get('ASM').add_filter('regtest', ASM_regtest)

