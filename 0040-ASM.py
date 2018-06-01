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
                self.reset()
        def reset(self):
                self.PC.set_word(0)
                self.SP.set_word(0x8000)
                self.memory = {}
        def set_PC(self, value):
                self.PC.set_word(value)
                if self.PC.value in self.memory:
                        code = self.memory[self.PC.value]
                        self.PC.color = code.color
                        instruction = self.by_code[code.value]
                        self.PC.char += " " + instruction.name
                        self.memory[self.PC.value].asm.rectangle()
        def step(self):
                if self.PC.value not in self.memory:
                        return
                instruction = self.by_code[self.memory[self.PC.value].value]
                instruction.execute(self)
                self.set_PC(self.PC.value + instruction.size + 1)
        def get_data_word(self):
                return (self.memory[self.PC.value+1].value * 256
                      + self.memory[self.PC.value+2].value)
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
                return block.rules[item.char](block, item)

def ASM_update_rule(block, rule):
        block.rules[rule[0]] = rule[1]
blocks.get('ASM').add_filter('update_rule', ASM_update_rule)

def ASM_set_time(block, t):
        block.t = t
        block.cpu.reset()
        block.variables = {}
        block.segment_heap = 0x8000
        block.segment_code = 0x0000
        block.segment_stack = 0x8020
        for i in range(block.segment_heap, block.segment_stack):
                block.cpu.memory[i] = Item('', 3*(i%4)).set_byte(0x00)
                block.cpu.memory[i].color = "#DDD"
                
        block.items = []
        if len(block.previous_block.items):
                asm_generate(block, block.previous_block.items[0])
        block.next_block.set_time(0)
blocks.get('ASM').add_filter('set_time', ASM_set_time)

def asm_Item(block, from_item, name, value='', codes=[]):
        item = from_item.clone()
        item.char = name + ' ' + value
        item.y = len(block.items)
        block.append(item)
        if name in block.cpu.by_name:
                instruction = block.cpu.by_name[name]
                if instruction.size != len(codes):
                        bug
                block.add_code(item.clone().set_byte(instruction.code))
                for code in codes:
                        block.add_code(item.clone().set_byte(code))

def asm_program(block, item):
        for child in item.children:
                asm_generate(block, child)

def asm_bytes(value):
        return [int(value) >> 8, int(value) & 0xFF]

def asm_affectation(block, item):
        asm_generate(block, item.children[1])
        variable_name = item.children[0].value
        addr = block.declare(item.children[0], variable_name)
        asm_Item(block, item, 'STORE AT ADDRESS', variable_name,
                 asm_bytes(addr))

def asm_value(block, item):
        value = item.children[0].value
        asm_Item(block, item.children[0], 'LOAD IMMEDIATE', value, [int(value)])

def asm_variable(block, item):
        variable_name = item.children[0].value
        if variable_name in block.variables:
                addr = block.variables[variable_name]
                block.cpu.memory[addr].previous_items.append(item.children[0])
        else:
                addr = 0xFFFF
        asm_Item(block, item.children[0], 'LOAD AT ADDRESS', variable_name,
                 asm_bytes(addr))
        if addr == 0xFFFF:
                block.items[-1].error = True

def asm_addition(block, item):
        asm_generate(block, item.children[0])
        asm_generate(block, item.children[1])
        asm_Item(block, item, 'ADDITION')

def asm_subtraction(block, item):
        if len(item.children) == 1:
                asm_generate(block, item.children[0])
                asm_Item(block, item, 'NEGATE')
        else:
                asm_generate(block, item.children[0])
                asm_generate(block, item.children[1])
                asm_Item(block, item, 'SUBTRACTION')

def asm_multiply(block, item):
        asm_generate(block, item.children[0])
        asm_generate(block, item.children[1])
        asm_Item(block, item, 'MULTIPLY')

def asm_divide(block, item):
        asm_generate(block, item.children[0])
        asm_generate(block, item.children[1])
        asm_Item(block, item, 'DIVIDE')

def ASM_dump(block, dummy_arg):
        block.dump_cpu_and_memory()
blocks.get('ASM').add_filter('dump', ASM_dump)
