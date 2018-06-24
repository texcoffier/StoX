"""GUI: update the URL to save the application state"""

def put_url_options(options):
        s = ''
        for option in options:
                if option[2] is None:
                        v = option[0]
                else:
                        v = option[0] + '·' + option[1] + '·' + option[2]
                s += '§' + v
        window.history.replaceState('', '', '#' + s[1:])

def update_url(block, data, method):
        options = get_url_options()
        ok = False
        for option in options:
                if option[0] == block.name and option[1] == method:
                        option[2] = data
                        ok = True
        if not ok:
                options.append([block.name, method, data])
        put_url_options(options)

def new_updater(block, method):
        def fct(block, data):
                update_url(block, data, method)
        block.add_filter(method, fct)

def update_url_hooks():
        for method in ['set', 'opened', 'fontsize', 'set_time', 'cursor',
                       'disabled']:
                new_updater(blocks, method)
                for block in blocks.blocks:
                        new_updater(block, method)
blocks.add_filter('final_init', update_url_hooks)

