class HasShift:
    def __init__(self, key1, key2):
        self.k1 = key1
        self.k2 = key2

class Vk2Sk(object):
    alt = "%"
    ctrl = "^"
    shift = "+"

    codes = {
        0x08: "{BKSP}",     # Backspace
        0x09: "{TAB}",      # Tab
        0x0D: "{ENTER}",    # Enter
        0x14: "{CAPSLOCK}",  # Caps lock
        0x1B: "{ESC}",      # Escape
        0x20: " ",          # Space
        0x21: "{PGUP}",     # Page up
        0x22: "{PGDN}",     # Page down
        0x23: "{END}",      # End
        0x24: "{HOME}",     # Home
        0x25: "{LEFT}",     # Left arrow
        0x26: "{UP}",       # Up arrow
        0x27: "{RIGHT}",    # Right arrow
        0x28: "{DOWN}",     # Down arrow
        0x2C: "{PRTSC}",    # Print Screen
        0x2D: "{INSERT}",   # Insert
        0x2E: "{DELETE}",   # Delete
        0x2F: "{HELP}",     # Help key
        0x30: HasShift("0", "{)}"),
        0x31: HasShift("1", "!"),
        0x32: HasShift("2", "@"),
        0x33: HasShift("3", "#"),
        0x34: HasShift("4", "$"),
        0x35: HasShift("5", "{%}"),
        0x36: HasShift("6", "{^}"),
        0x37: HasShift("7", "&"),
        0x38: HasShift("8", "*"),
        0x39: HasShift("9", "{(}"),
        0x41: "A",
        0x42: "B",
        0x43: "C",
        0x44: "D",
        0x45: "E",
        0x46: "F",
        0x47: "G",
        0x48: "H",
        0x49: "I",
        0x4A: "J",
        0x4B: "K",
        0x4C: "L",
        0x4D: "M",
        0x4E: "N",
        0x4F: "O",
        0x50: "P",
        0x51: "Q",
        0x52: "R",
        0x53: "S",
        0x54: "T",
        0x55: "U",
        0x56: "V",
        0x57: "W",
        0x58: "X",
        0x59: "Y",
        0x5A: "Z",
        0x60: "0",      # Numpad keys
        0x61: "1",
        0x62: "2",
        0x63: "3",
        0x64: "4",
        0x65: "5",
        0x66: "6",
        0x67: "7",
        0x68: "8",
        0x69: "9",
        0x6A: "{MULTIPLY}",  # Keypad multiply
        0x6B: "{ADD}",       # Keypad add
        0x6D: "{SUBTRACT}",  # Keypad subtract
        0x6E: ".",           # Keypad decimal
        0x6F: "{DIVIDE}",    # Keypad divide
        0x70: "{F1}",
        0x71: "{F2}",
        0x72: "{F3}",
        0x73: "{F4}",
        0x74: "{F5}",
        0x75: "{F6}",
        0x76: "{F7}",
        0x77: "{F8}",
        0x78: "{F9}",
        0x79: "{F10}",
        0x7A: "{F11}",
        0x7B: "{F12}",
        0x7C: "{F13}",
        0x7D: "{F14}",
        0x7E: "{F15}",
        0x7F: "{F16}",
        0x80: "{F17}",
        0x81: "{F18}",
        0x82: "{F19}",
        0x83: "{F20}",
        0x84: "{F21}",
        0x85: "{F22}",
        0x86: "{F23}",
        0x87: "{F24}",
        0x90: "{NUMLOCK}",      # Num lock key
        0x91: "{SCROLLLOCK}",   # Scroll lock key
        0xBA: HasShift(";", ":"),
        0xBB: HasShift("=", "{+}"),
        0xBC: HasShift(",", "<"),
        0xBD: HasShift("-", "_"),
        0xBE: HasShift(".", ">"),
        0xBF: HasShift("/", "?"),
        0xDB: HasShift("{[}", "{{}"),
        0xDC: HasShift("|", "\\"),
        0xDD: HasShift("{]}", "{}}"),
        0xDE: HasShift("'", "\"")
    }

    @staticmethod
    def convert(key_code, alt=False, ctrl=False, shift=False):
        ret = ""
        if alt:
            ret += Vk2Sk.alt

        if ctrl:
            ret += Vk2Sk.ctrl

        if shift:
            ret += Vk2Sk.shift

        if key_code in Vk2Sk.codes:
            ret += Vk2Sk.codes[key_code]
        else:
            return "Bad value: " + hex(key_code)
        return ret


