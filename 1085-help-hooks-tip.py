"""GUI help: displays an hook tip listing the functionalities"""

def help_hooks_tip_text(name):
        s = 'Defined by:<ul>'
        for f in functionalities_hook_defined:
                if name in functionalities_hook_defined[f]:
                        s += '<li>' + f
        s += '</ul>Used by:<ul>'
        for f in functionalities_hook_used:
                if name in functionalities_hook_used[f]:
                        s += '<li>' + f
        s += '</ul>'
        return s
        
def help_hooks_tip(blocks, help_window):
        help_window['style'] += """
        .hook_name { display: inline-block ; }
        .hook_name DIV {
                        display: none;
                        position: absolute;
                        background: #FFF;
                        color: #000;
                        border: 1px solid black;
                        font-size: 120%;
                        padding: 1em;
        }
        .hook_name UL { padding-left: 1em; }
        .hook_name:hover { color: #FFF ; background: #000 }
        .hook_name:hover DIV { display: block ; }
        """
        for line in help_window['table-content']:
                f = line[1]
                for i in [4, 5]:
                        s = ''
                        for hook in line[i].split(' '):
                              s += ('<div class="hook_name">' + hook
                                     + '<div>' + help_hooks_tip_text(hook)
                                     + '</div></div> ')
                        line[i] = s
blocks.add_filter('update_help', help_hooks_tip)
