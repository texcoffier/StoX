"""GUI: the open/close block icon"""

def open_close_event(event):
        for block in blocks.blocks:
                if block.open_close_button is event.target:
                        block.call('opened', 1 - block.is_open)
                        break

def opened(block, state):
        block_open_close(block, state)
        nr_open = 0
        for block in blocks.blocks:
                if block.window_top and block.is_open:
                        nr_open += 1
        closed_size = 2
        blocks.real_width = (100 - (blocks.nr_columns - nr_open) * closed_size
                ) / nr_open
        width = blocks.real_width + '%'
        blocks.real_width *= blocks.element.offsetWidth / 100
        for block in blocks.blocks:
                if not block.window_top:
                        continue
                div = block.element.parentNode
                if block.is_open:
                        div.style.width = width
                        div.className = 'opened'
                else:
                        div.style.width = closed_size + '%'
                        div.className = 'closed'

def block_open_close(block, is_open):
        block.is_open = is_open
        block.open_close_button.innerHTML = is_open and "▶" or "▼"

def open_close_behavior(block, dummy):
        if not block.window_top:
                return
        block.open_close_button = document.createElement('SPAN')
        block.open_close_button.className = 'open_close'
        block.open_close_button.onclick = open_close_event
        block.buttons.appendChild(block.open_close_button)
        block_open_close(block, 1)

for block in blocks.blocks:
        block.add_filter('html_init', open_close_behavior)
        block.add_filter('opened', opened)

def open_close_style(blocks, dummy):
        style = document.createElement("STYLE")
        style.textContent = """
        .open_close { color: #88F; cursor: pointer; }
        .header:hover .open_close { color: #00F; }
        DIV.closed CANVAS { opacity: 0.3; }
        DIV.closed .time_travel { display: none; }
        BODY > DIV > DIV { transition: width 1s; }
        DIV CANVAS { transition: opacity 0.3s; }
        """
        body.appendChild(style)
blocks.add_filter('html_init', open_close_style)
