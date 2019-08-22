# -*- coding: utf-8 -*-

from prompt_toolkit import keys
keys.Keys.ControlF1 = 'c-f1'
keys.Keys.ControlF2 = 'c-f2'
#keys.Keys.ControlF3 = 'c-f3'
keys.Keys.ControlF4 = 'c-f4'
keys.Keys.ControlF5 = 'c-f5'
keys.Keys.ControlF6 = 'c-f6'
keys.Keys.ControlF7 = 'c-f7'
keys.Keys.ControlF8 = 'c-f8'
keys.Keys.ControlF9 = 'c-f9'
keys.Keys.ControlF10 = 'c-f10'
keys.Keys.ControlF11 = 'c-f11'
keys.Keys.ControlF12 = 'c-f12'

from prompt_toolkit.input.ansi_escape_sequences import ANSI_SEQUENCES
ANSI_SEQUENCES.update({
    '\x1b[O5P': keys.Keys.ControlF1,
    '\x1b[O5Q': keys.Keys.ControlF2,
#    '\x1b[O5R': keys.Keys.ControlF3,
    '\x1b[O5S': keys.Keys.ControlF4,
    '\x1b[1;5P': keys.Keys.ControlF1,
    '\x1b[1;5Q': keys.Keys.ControlF2,
#    '\x1b[1;5R': keys.Keys.ControlF3, # ???
    '\x1b[1;5S': keys.Keys.ControlF4,
    '\x1b[15;5~': keys.Keys.ControlF5,
    '\x1b[17;5~': keys.Keys.ControlF6,
    '\x1b[18;5~': keys.Keys.ControlF7,
    '\x1b[19;5~': keys.Keys.ControlF8,
    '\x1b[20;5~': keys.Keys.ControlF9,
    '\x1b[21;5~': keys.Keys.ControlF10,
    '\x1b[23;5~': keys.Keys.ControlF11,
    '\x1b[24;5~': keys.Keys.ControlF12,
})

keys.KEY_ALIASES.update({
    's-f1': 'f13',
    's-f2': 'f14',
#    's-f3': 'f15',
    's-f4': 'f16',
    's-f5': 'f17',
    's-f6': 'f18',
    's-f7': 'f19',
    's-f8': 'f20',
    's-f9': 'f21',
    's-f10': 'f22',
    's-f11': 'f23',
    's-f12': 'f24',
})

XTERM_KEYS = [getattr(keys.Keys, k) for k in dir(keys.Keys) if not (k.startswith('_') or k in keys.ALL_KEYS)]

keys.ALL_KEYS += XTERM_KEYS
