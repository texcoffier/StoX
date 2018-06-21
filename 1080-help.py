"""GUI: displays the help window"""

def help_key(blocks, event):
        blocks.a_key_is_pressed = event.key != 'Control'
blocks.add_filter('key', help_key)

def help_keyup(blocks, event):
        if blocks.a_key_is_pressed is False:
                blocks.help.style.opacity = 0.9
                blocks.help.style.transition = "opacity 0.5s"
                blocks.help.style.pointerEvents = 'initial'
        else:
                blocks.help.style.opacity = 0
                blocks.help.style.pointerEvents = 'none'
                if event and event.key == 'Escape':
                        return # Do not record changes
                blocks.call('help_change', event)
blocks.add_filter('keyup', help_keyup)

def help_html_init(blocks, dummy):
        if not body:
                return
        help_window = {}
        help_window['title'] = "<h1>Hit «Control» key to see this box</h1>"
        help_window['style'] = """
.help {
        position: absolute;
        right: 10%;
        left: 10% ;
        top: 10%;
        bottom: 10% ;
        opacity: 1;
        background: #FFE ;
        border: 1px solid black;
        transition: opacity 3s ;
        overflow: auto ;
        padding: 0.5em ;
      }
.help H1 { text-align: center ; }
.help TABLE {
        border-spacing: 0px;
        border: 1px solid black;
        width: 99% ;
        margin: 1em ;
}
.help TABLE TD {
        border: 1px solid black;
        white-space: normal;
}
.help TD.id {
        white-space: nowrap ;
        width: 10% ;
}
"""
        help_window['table-content'] = []
        help_window['table-columns-class'] = ['priority', 'key', 'id', 'doc']
        for f in functionalities:
                help_window['table-content'].append([
                                functionalities[f],  # Sort key
                                f,                   # Functionality ID
                                f,                   # First column (ID)
                                functionalities[f]   # Second column (doc)
                                ])

        blocks.call('update_help', help_window)

        style = document.createElement('STYLE')
        style.textContent = help_window['style']
        body.appendChild(style)
        blocks.help = document.createElement('DIV')
        blocks.help.className = 'help'
        lines = ['<table>']
        help_window['table-content'].sort()
        for line in help_window['table-content']:
                s = '<tr>'
                for i, col in enumerate(help_window['table-columns-class']):
                        if i >= 2:
                                s += '<td class="' + col + '">' + line[i]
                s += '</tr>'
                lines.append(s)
        lines.append('</table>')
        blocks.help.innerHTML = help_window['title'] + join(lines, '')
        body.appendChild(blocks.help)
blocks.add_filter('html_init', help_html_init)

blocks.add_filter('final_init', help_keyup)


