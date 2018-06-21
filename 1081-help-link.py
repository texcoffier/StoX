"""GUI: add links to the functionality source file"""

def help_links(blocks, help_window):
        for line in help_window['table-content']:
                f = line[1]
                line[2] = ('<a href="TMP/' + f
                      + '.py.html" mimetype="text/html;charset=UTF-8" >'
                      + line[2] + '</a>')
blocks.add_filter('update_help', help_links)
