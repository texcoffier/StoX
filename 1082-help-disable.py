"""GUI: add the disable toggle to the help window"""

def help_change(blocks, event):
        inputs = blocks.help.getElementsByTagName('INPUT')
        new_disabled = []
        for i in inputs:
                if not i.checked:
                        new_disabled.append(i.name)
        disabled_functionalities.sort()
        new_disabled.sort()
        if disabled_functionalities != new_disabled:
                s = ''
                for i in new_disabled:
                        s += '-' + i
                blocks.call('disabled', s)
                window.location.reload()
blocks.add_filter('help_change', help_change)

def help_disable(blocks, help_window):
        help_window['style'] += '''
.help INPUT:checked + DIV {
        background: initial ;
}
.help INPUT + DIV {
        background: #FDD ;
}
.help INPUT + DIV {
        display: inline ;
}'''
        for line in help_window['table-content']:
                f = line[1]
                if f in disabled_functionalities:
                        v = ''
                else:
                        v = ' checked'
                        if required[f]:
                                v += ' disabled'
                line[3] = ('<input type="checkbox"' + v + ' name="' + f + '">'
                           + line[3])
blocks.add_filter('update_help', help_disable)
