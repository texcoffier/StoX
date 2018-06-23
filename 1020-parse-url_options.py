"""GUI: parse the options in the URL"""

def get_url_options():
        options = []
        if window.location.hash == '':
                return options
        for item in decodeURIComponent(window.location.hash[1:]).split("§"):
                block_name, method, value = item.split('·')
                if value is None:
                        options.append([item, None, None])
                else:
                        options.append([block_name, method, value])
        return options

def parse_url_options():
        for block_name, method, value in get_url_options():
                if value is None:
                        continue
                if value != '' and not isNaN(value):
                        value = int(value)
                try:
                        block = eval(block_name)
                        if method in block.methods:
                                block.call(method, value)
                        else:
                                setattr(block, method, value)
                except:
                        print(block_name, method, value)
blocks.add_filter('final_init', parse_url_options)
