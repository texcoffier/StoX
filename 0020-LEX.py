class LEX(Block):
        title = "Lexical analyser"
        name = "LEX"
blocks.append(LEX())

blocks.get('LEX').add_filter('html_init', canvas_html_init)
blocks.get('LEX').add_filter('html_draw', SRC_html_draw)

def LEX_dump(block, dummy_args):
        dump_item = block.get_filter('dumpitem')
        for item in block.items:
                item.dump()
                for function in dump_item:
                        function(item)
blocks.get('LEX').add_filter('dump', LEX_dump)

def LEX_init(block, dummy):
        block.lexem = []
        for lexem in [
                ['word'        , '[a-zA-Z]+'   , '#088'],
                ['number'      , '[0-9]+'      , '#880'],
                ['separator'   , '[ \n\t]'     , '#000'],
                ['plus'        , '[+]'         , '#808'],
                ['minus'       , '[-]'         , '#808'],
                ['star'        , '[*]'         , '#808'],
                ['slash'       , '[/]'         , '#808'],
                ['affectation' , '[=]'         , '#F00'],
                ['open'        , '[(]'         , '#00F'],
                ['close'       , '[)]'         , '#00F']
        ]:
                block.call('add_lexem', lexem)
blocks.get('LEX').add_filter('init', LEX_init)

class Lexem:
        def __init__(self, data):
                self.name   = data[0]
                self.regexp = data[1]
                self.color  = data[2]
        def long(self):
                return self.name + ':' + self.regexp

def LEX_add_lexem(block, lexem):
        block.lexem.append(Lexem(lexem))
blocks.get('LEX').add_filter('add_lexem', LEX_add_lexem)

def LEX_set_time(block, t):
        block.t = t
        items = block.previous_block.items
        block.items = []
        previous_items = []
        previous_possibles = []
        previous_current = ''
        current = ''
        i = 0
        # The loop go too far in order to output the last lexem
        while i <= len(items):
                if False:
                        print('i=', i,
                              'p_items=',
                               join([i.short() for i in previous_items]),
                              'p_possibles=',
                               join([i.long() for i in previous_possibles]),
                              'p_current=', previous_current
                              )
                possibles = []
                if i != len(items):
                        item = items[i]
                        current += item.char
                        for lexem in block.lexem:
                                if match(lexem.regexp, current):
                                        possibles.append(lexem)
                        item.possibles = possibles
                if len(possibles) == 0:
                        if len(previous_possibles) == 1:
                                lexem = previous_possibles[0]
                                item = Item('', 0, len(block.items),
                                            previous_items)
                                item.rule  = lexem.name
                                item.value = previous_current
                                item.char  = (backslash(item.value)
                                              + ' (' + item.rule
                                              + ':' + backslash(lexem.regexp)
                                              + ')')
                                item.color       = lexem.color
                                block.append(item)
                                current = ''
                                previous_items = []
                                previous_possibles = block.lexem # All possibles
                                previous_current = ''
                        else:
                                if current != '':
                                        item = Item(current + ':UNEXPECTED',
                                            0, len(block.items),
                                            previous_items)
                                        item.previous_items = items[i:]
                                        item.color = "#F00"
                                        item.error = True
                                        block.append(item)
                                break
                else:
                        i += 1
                        previous_items.append(item)
                        previous_possibles = possibles
                        previous_current = current
        block.next_block.set_time(0)
blocks.get('LEX').add_filter('set_time', LEX_set_time)
