"""GUI help: display defined and used hooks"""

def help_hooks(blocks, help_window):
        help_window['table-columns-class'].append('hook_defined')
        help_window['table-columns-class'].append('hook_used')
        help_window['style'] += """
        .hook_defined, .hook_used { font-size: 65%; width: 20em }
        """
        for line in help_window['table-content']:
                f = line[1]
                line.append(join(functionalities_hook_defined[f], ' '))
                line.append(join(functionalities_hook_used[f], ' '))
blocks.add_filter('update_help', help_hooks)
