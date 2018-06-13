class _LEX_(Block):
        title = "Lexical analyser"
        name = "LEX"
LEX = blocks.append(_LEX_())

LEX.add_filter('html_init', canvas_html_init)
LEX.add_filter('html_draw', SRC_html_draw)

def LEX_dump(block, dummy_args):
        dump_item = block.get_filter('dumpitem')
        for item in block.items:
                item.dump()
                for function in dump_item:
                        function(item)
LEX.add_filter('dump', LEX_dump)

def LEX_init(block, dummy):
        block.lexem = []
        block.lexem_by_rule = {}
        for lexem in [
                [100, 'word'        , '[ \n\t]*[a-zA-Z]+[ \n\t]*', '#088'],
                [100, 'number'      , '[ \n\t]*[0-9]+[ \n\t]*'   , '#880'],
                [100, 'plus'        , '[ \n\t]*[+][ \n\t]*'      , '#808'],
                [100, 'minus'       , '[ \n\t]*[-][ \n\t]*'      , '#808'],
                [100, 'star'        , '[ \n\t]*[*][ \n\t]*'      , '#808'],
                [100, 'slash'       , '[ \n\t]*[/][ \n\t]*'      , '#808'],
                [100, 'affectation' , '[ \n\t]*[=][ \n\t]*'      , '#F00'],
                [100, 'open'        , '[ \n\t]*[(][ \n\t]*'      , '#00F'],
                [100, 'close'       , '[ \n\t]*[)][ \n\t]*'      , '#00F'],
                [999, 'nothing'     , '[ \n\t]+'                 , '#000']
        ]:
                block.call('update_lex', lexem)
LEX.add_filter('init', LEX_init)

class Lexem:
        def __init__(self, data):
                self.priority = data[0]
                self.name     = data[1]
                self.regexp   = data[2]
                self.color    = data[3]
        def long(self):
                return self.name + ':' + self.regexp

def lex_compare_js(x, y):
        return x.priority - y.priority
def lex_compare_python(x):
        return x.priority

def LEX_update_lex(block, lexem):
        l = Lexem(lexem)
        block.lexem.append(l)
        block.lexem_by_rule[l.name] = l
        if context == "JavaScript":
                block.lexem.sort(lex_compare_js)
        else:
                block.lexem.sort(key=lex_compare_python)
LEX.add_filter('update_lex', LEX_update_lex)

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
                        if (len(previous_possibles) >= 1
                             and current != ''
                             and len(previous_possibles) != len(block.lexem)):
                                lexem = previous_possibles[0]
                                item = Item('', 0, len(block.items),
                                            previous_items)
                                item.rule  = lexem.name
                                item.value = strip(previous_current)
                                item.char  = (backslash(item.value)
                                              + ' → ' + item.rule)
                                item.color       = lexem.color
                                block.append(item)
                                current = ''
                                previous_items = []
                                previous_possibles = block.lexem # All possibles
                                previous_current = ''
                        else:
                                if current != '':
                                        item = Item(current + ' is UNEXPECTED',
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
        block.next_block.set_time(-1)
LEX.add_filter('set_time', LEX_set_time)

def LEX_html_draw(block, dummy):
        for item in block.items:
                if item.highlight and item.rule in block.lexem_by_rule:
                        feedback = Item('', 0, len(block.items) + 1)
                        feedback.block = block
                        for text in ['Rule:',
                                     item.rule,
                                     '',
                                     'Priority:',
                                     block.lexem_by_rule[item.rule].priority,
                                     '',
                                     'Regular expression:',
                                     block.lexem_by_rule[item.rule].regexp
                                     ]:
                                feedback.char = text
                                feedback.fillText()
                                feedback.y += 1
        SRC.cursor

LEX.add_filter('html_draw', LEX_html_draw)


def LEX_regtest(lex, dummy):
        SRC.call('set', 'a$7')
        for i, expected in enumerate([
        '0×0:a → word<word>,previous=0×0:a<a>',
        '0×1:$ is UNEXPECTED<$ is UNEXPECTED>,previous=1×0:$<$>·2×0:7<7>',
        ]):
                if lex.items[i].long() != backslash(expected):
                        print(expected)
                        print(lex.items[i].long())
                        bug
LEX.add_filter('regtest', LEX_regtest)
