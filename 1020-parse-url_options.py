
def parse_url_options():
        if window.location.hash == '':
                return
        for item in decodeURIComponent(window.location.hash[1:]).split("§"):
                block_name, method, value = item.split('·')
                if value is None:
                        print(item)
                        continue
                if not isNaN(value):
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
