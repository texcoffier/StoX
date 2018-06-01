class ASM(Block):
        title = "Assembly language"
        name = "ASM"
        def declare(self, item, variable):
                if variable not in self.variables:
                        self.variables[variable] = self.nr_variables
                        self.nr_variables += 1
                        asm_Item(self, item, '.HEAP # keep 2 bytes for «'
                                 + variable + '»')
                        self.heap.append(item.clone().set_byte(0))
                return self.variables[variable]
blocks.append(ASM())

blocks.get('ASM').add_filter('dump', LEX_dump)
blocks.get('ASM').add_filter('html_init', canvas_html_init)
blocks.get('ASM').add_filter('html_draw', SRC_html_draw)

class Instruction:
        def __init__(self, code, name, size):
                self.block = blocks.get('ASM')
                self.code = code
                self.name = name
                self.size = size
                self.block.by_code[code] = self
                self.block.by_name[name] = self

def ASM_init(block, dummy):
        block.rules = {}
        block.by_code = {}
        block.by_name = {}
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
        Instruction(0x00, "LOAD IMMEDIATE"  , 2)
        Instruction(0x01, "STORE AT ADDRESS", 2)
        Instruction(0x02, "LOAD AT ADDRESS" , 2)
        Instruction(0x03, "ADDITION"        , 0)
        Instruction(0x04, "SUBTRACTION"     , 0)
        Instruction(0x05, "MULTIPLY"        , 0)
        Instruction(0x06, "DIVIDE"          , 0)
        Instruction(0x07, "NEGATE"          , 0)

blocks.get('ASM').add_filter('init', ASM_init)

def asm_generate(block, item):
        if item.char in block.rules:
                return block.rules[item.char](block, item)

def ASM_update_rule(block, rule):
        block.rules[rule[0]] = rule[1]
blocks.get('ASM').add_filter('update_rule', ASM_update_rule)

def ASM_set_time(block, t):
        block.variables = {}
        block.code = []
        block.heap = []
        block.nr_variables = 0
        block.t = t
        if len(block.previous_block.items):
                block.items = []
                asm_generate(block, block.previous_block.items[0])
blocks.get('ASM').add_filter('set_time', ASM_set_time)

def asm_Item(block, from_item, name, value='', codes=[]):
        item = from_item.clone()
        item.char = name + ' ' + value
        item.y = len(block.items)
        if name in block.by_name:
                instruction = block.by_name[name]
                if instruction.size != len(codes):
                        bug
                block.code.append(item.clone().set_byte(instruction.code))
                for code in codes:
                        block.code.append(item.clone().set_byte(code))
        block.append(item)

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
        asm_Item(block, item.children[0], 'LOAD IMMEDIATE', value,
                 asm_bytes(value))

def asm_variable(block, item):
        variable_name = item.children[0].value
        if variable_name in block.variables:
                addr = block.variables[variable_name]
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
        print('<code>')
        for item in block.code:
                print('\t', item.char)
        print('</code>')
        print('<heap>')
        for item in block.heap:
                print('\t', item.char)
        print('</heap>')
blocks.get('ASM').add_filter('dump', ASM_dump)
