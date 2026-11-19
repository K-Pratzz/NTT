#!/usr/bin/env python3
"""
Hack assembler -- Nand to Tetris I capstone, Part B.

K = 23  ->  K mod 3 = 2  ->  extra feature: print a WARNING if the same
label is defined more than once.

Usage:   python assembler.py Prog.asm
Output:  Prog.hack  (written next to the input file)

How it works (two readings of the file):
  First reading : strip comments/blank lines, and record the ROM address
                  of every label like (LOOP).  Labels do not produce code.
  Second reading: translate each remaining line into 16 bits.
                  A-instruction  @value  -> 0 + 15-bit binary number
                  C-instruction  dest=comp;jump -> 111 a cccccc ddd jjj
                  A symbol that is not predefined and not a label is a
                  variable: it gets RAM addresses 16, 17, 18, ... in the
                  order it first appears.
"""
import sys
import os

# ---------------------------------------------------------------- tables
# comp field = a-bit (1 if M is used) + six c-bits
COMP = {
    '0': '0101010', '1': '0111111', '-1': '0111010',
    'D': '0001100', 'A': '0110000', '!D': '0001101', '!A': '0110001',
    '-D': '0001111', '-A': '0110011', 'D+1': '0011111', 'A+1': '0110111',
    'D-1': '0001110', 'A-1': '0110010', 'D+A': '0000010', 'D-A': '0010011',
    'A-D': '0000111', 'D&A': '0000000', 'D|A': '0010101',
    'M': '1110000', '!M': '1110001', '-M': '1110011', 'M+1': '1110111',
    'M-1': '1110010', 'D+M': '1000010', 'D-M': '1010011', 'M-D': '1000111',
    'D&M': '1000000', 'D|M': '1010101',
}
# same operations written in the other order (A+D is the same as D+A, ...)
COMP_ALIASES = {'A+D': 'D+A', 'M+D': 'D+M', 'A&D': 'D&A', 'M&D': 'D&M',
                'A|D': 'D|A', 'M|D': 'D|M'}

JUMP = {'': '000', 'JGT': '001', 'JEQ': '010', 'JGE': '011',
        'JLT': '100', 'JNE': '101', 'JLE': '110', 'JMP': '111'}

# predefined symbols
SYMBOLS = {'SP': 0, 'LCL': 1, 'ARG': 2, 'THIS': 3, 'THAT': 4,
           'SCREEN': 16384, 'KBD': 24576}
for i in range(16):
    SYMBOLS['R%d' % i] = i


class AsmError(Exception):
    pass


def dest_bits(dest):
    """dest letters A, D, M in any order -> 3 bits (A D M)."""
    if any(ch not in 'ADM' for ch in dest) or len(set(dest)) != len(dest):
        raise AsmError('invalid destination "%s"' % dest)
    return ''.join('1' if ch in dest else '0' for ch in 'ADM')


def clean(line):
    """Remove comment and all whitespace."""
    return ''.join(line.split('//')[0].split())


# ---------------------------------------------------------------- pass 1
def first_pass(lines):
    """Return (instructions, symbol table).
    instructions = list of (source line number, text without spaces)."""
    symbols = dict(SYMBOLS)
    label_line = {}          # label -> line where it was first defined
    instructions = []
    for number, raw in enumerate(lines, start=1):
        text = clean(raw)
        if not text:
            continue
        if text.startswith('('):
            if not text.endswith(')') or len(text) < 3:
                raise AsmError('Line %d: invalid label "%s"' % (number, text))
            label = text[1:-1]
            # ---- EXTRA FEATURE (K mod 3 == 2): duplicate label warning
            if label in label_line:
                print('WARNING: Line %d: label (%s) already defined on '
                      'line %d' % (number, label, label_line[label]),
                      file=sys.stderr)
            else:
                label_line[label] = number
                symbols[label] = len(instructions)   # next ROM address
        else:
            instructions.append((number, text))
    return instructions, symbols


# ---------------------------------------------------------------- pass 2
def translate_a(number, text, symbols, next_var):
    name = text[1:]
    if name == '':
        raise AsmError('Line %d: empty @ instruction' % number)
    if name.isdigit():
        value = int(name)
    else:
        if name[0].isdigit():
            raise AsmError('Line %d: invalid symbol "%s"' % (number, name))
        if name not in symbols:                 # new variable
            symbols[name] = next_var[0]
            next_var[0] += 1
        value = symbols[name]
    if value > 32767:
        raise AsmError('Line %d: address %d too large' % (number, value))
    return '0' + format(value, '015b')


def translate_c(number, text):
    dest, comp, jump = '', text, ''
    if '=' in comp:
        dest, comp = comp.split('=', 1)
    if ';' in comp:
        comp, jump = comp.split(';', 1)
    comp = COMP_ALIASES.get(comp, comp)
    if comp not in COMP:
        raise AsmError('Line %d: invalid instruction "%s"' % (number, text))
    if jump not in JUMP:
        raise AsmError('Line %d: invalid jump "%s"' % (number, jump))
    try:
        d = dest_bits(dest)
    except AsmError as e:
        raise AsmError('Line %d: %s' % (number, e))
    return '111' + COMP[comp] + d + JUMP[jump]


def assemble(lines):
    instructions, symbols = first_pass(lines)
    next_var = [16]                              # next free RAM address
    out = []
    for number, text in instructions:
        if text.startswith('@'):
            out.append(translate_a(number, text, symbols, next_var))
        else:
            out.append(translate_c(number, text))
    return out


def main():
    if len(sys.argv) != 2 or not sys.argv[1].endswith('.asm'):
        print('Usage: python assembler.py Prog.asm')
        sys.exit(1)
    path = sys.argv[1]
    with open(path) as f:
        lines = f.read().splitlines()
    try:
        code = assemble(lines)
    except AsmError as e:
        print('ERROR:', e)
        sys.exit(1)
    out_path = os.path.splitext(path)[0] + '.hack'
    with open(out_path, 'w') as f:
        f.write('\n'.join(code) + '\n')
    print('Wrote %d instructions to %s' % (len(code), out_path))


if __name__ == '__main__':
    main()
