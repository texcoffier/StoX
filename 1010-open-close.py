
def block_open_close_toggle(event):
        for block in blocks.blocks:
                if block.name == event.target.className:
                        block_open_close(block, 1 - block.is_open)
        nr_open = 0
        for block in blocks.blocks:
                if block.is_open:
                        nr_open += 1
        closed_size = 2
        width = (100 - (len(blocks.blocks)-nr_open) * closed_size) / nr_open + '%'
        for block in blocks.blocks:
                div = block.element.parentNode
                if block.is_open:
                        div.style.width = width
                        div.className = 'opened'
                else:
                        div.style.width = closed_size + '%'
                        div.className = 'closed'

def block_open_close(block, is_open):
        block.is_open = is_open
        block.title.firstChild.innerHTML = is_open and "▶" or "▼"

def open_close_behavior(block, dummy):
        block.title = block.element.parentNode.firstChild
        block.title.innerHTML = (
        '<span onclick="block_open_close_toggle(event)" class="'
        + block.name + '"></span>' + block.title.innerHTML)
        block_open_close(block, 1)

def open_close_style(blocks, dummy):
        style = document.createElement("STYLE")
        style.textContent = """
        .title SPAN { color: #88F; cursor: pointer; }
        .title:hover SPAN { color: #00F; }
        .title { background: #EEF; }
        DIV.closed CANVAS { opacity: 0.3; }
        BODY > DIV > DIV { transition: width 1s; }
        DIV CANVAS { transition: opacity 0.3s; }
        """
        body.appendChild(style)
blocks.add_filter('html_init', open_close_style)

for block in blocks.blocks:
        block.add_filter('html_init', open_close_behavior)

