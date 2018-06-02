###############################################################################
# Utilities
###############################################################################

def backslash(txt):
        return txt.replace('\n','\\n').replace('\t','\\t')

def hex(integer):
        return "0123456789ABCDEF"[integer & 15]

def clamp(integer):
        i = integer & 0xFF
        if i >= 128:
                return -256 + i
        else:
                return i
