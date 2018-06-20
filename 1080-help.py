"""GUI: displays the help window"""

def help_key(blocks, event):
        blocks.a_key_is_pressed = event.key != 'Control'
blocks.add_filter('key', help_key)

def help_keyup(blocks, dummy):
        if blocks.a_key_is_pressed is False:
                blocks.help.style.opacity = 0.9
                blocks.help.style.transition = "opacity 0.5s"
                blocks.help.style.pointerEvents = 'initial'
        else:
                blocks.help.style.opacity = 0
                blocks.help.style.pointerEvents = 'none'
blocks.add_filter('keyup', help_keyup)

def help_html_init(blocks, dummy):
        if not body:
                return
        style = document.createElement('STYLE')
        style.textContent = """
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
        body.appendChild(style)
        
        blocks.help = document.createElement('DIV')
        blocks.help.className = 'help'
        s = []
        for f in functionalities:
                s.append('<!--' + functionalities[f] + '-->'
                         + '<tr><td class="id">' + f
                         + '<td>' + functionalities[f] + '</tr>')
        s.sort()
        blocks.help.innerHTML = '''<h1>Hit «Control» key to see this box</h1>
        <table>''' + join(s, '') + '</table>'
        body.appendChild(blocks.help)
blocks.add_filter('html_init', help_html_init)


blocks.add_filter('final_init', help_keyup)


