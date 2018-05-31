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
blocks.append(ASM())

blocks.get('ASM').add_filter('dump', LEX_dump)
blocks.get('ASM').add_filter('html_init', canvas_html_init)
blocks.get('ASM').add_filter('html_draw', SRC_html_draw)

def ASM_init(block, dummy):
        block.rules = {}
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

def asm_Item(block, from_item, name, codes=[]):
        item = from_item.clone()
        item.char = name
        item.y = len(block.items)
        for code in codes:
                block.code.append(item.clone().set_byte(code))
        block.append(item)

def asm_program(block, item):
        for child in item.children:
                asm_generate(block, child)

def asm_affectation(block, item):
        asm_generate(block, item.children[1])
        block.declare(item.children[0], item.children[0].value)
        asm_Item(block, item, '    STORE AT ADDRESS ' + item.children[0].value)

def asm_value(block, item):
        value = item.children[0].value
        asm_Item(block, item.children[0], '    LOAD IMMEDIATE ' + value,
                 [0, int(value) >> 8, int(value) & 0xFF]
                )

def asm_variable(block, item):
        asm_Item(block, item.children[0], '    LOAD AT ADDRESS ' + item.children[0].value)

def asm_addition(block, item):
        asm_generate(block, item.children[0])
        asm_generate(block, item.children[1])
        asm_Item(block, item, '    ADDITION')

def asm_subtraction(block, item):
        if len(item.children) == 1:
                asm_generate(block, item.children[0])
                asm_Item(block, item, '    NEGATE')
        else:
                asm_generate(block, item.children[0])
                asm_generate(block, item.children[1])
                asm_Item(block, item, '    SUBTRACTION')

def asm_multiply(block, item):
        asm_generate(block, item.children[0])
        asm_generate(block, item.children[1])
        asm_Item(block, item, '    MULTIPLY')

def asm_divide(block, item):
        asm_generate(block, item.children[0])
        asm_generate(block, item.children[1])
        asm_Item(block, item, '    DIVIDE')

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
