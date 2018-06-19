"""Core utility: basic functions"""

def hex(integer):
        return "0123456789ABCDEF"[integer & 15]

def hex4(integer):
        return hex(integer>>12) + hex(integer>>8) + hex(integer>>4) + hex(integer)

def clamp(integer):
        i = integer & 0xFF
        if i >= 128:
                return -256 + i
        else:
                return i
