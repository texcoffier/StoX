"""GUI: the buttons to change font size"""

def font_size_buttons(block, dummy):
        block.font_size_button = document.createElement('DIV')
        block.font_size_button.className = 'time_travel fontsize'
        block.font_size_button.innerHTML = '<button>A</button><button>A</button>'
        def bigger():
                update_font_size(block.element, '+')
        def smaller():
                update_font_size(block.element, '-')
        block.font_size_button.firstChild.onclick = smaller
        block.font_size_button.lastChild.onclick = bigger
        block.buttons.appendChild(block.font_size_button)

for block in blocks.blocks:
        block.add_filter('html_init', font_size_buttons)

def font_size_button_style(blocks, dummy):
        style = document.createElement("STYLE")
        style.textContent = """
        .fontsize BUTTON:first-child { margin-right: 0px ; font-size: 70% }
        .fontsize BUTTON:last-child { margin-left: 0px ; }
        """
        body.appendChild(style)
blocks.add_filter('html_init', font_size_button_style)
