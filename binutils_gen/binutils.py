import os
import argparse
from sys import argv

from pyrametros import CFile, parse_file

from binutils_gen.opcode import NemaWeaverOpcode, check_duplicates
from binutils_gen.isa import InstructionSet

DEFAULT_OPC = "/homes/cperivol/Projects/binutils_gen/binutils_gen/test/nemaweaver-opc.h"
DEFAULT_OPCM = "/homes/cperivol/Projects/binutils_gen/binutils_gen/test/nemaweaver-opcm.h"
DEFAULT_ISA = "/homes/cperivol/Projects/Nema/NemaSpec/Nema_ISA.txt"

def main():
    # You may want to run
    # python binutils.py Nema_ISA.txt ../nemaweaver-binutils/opcodes/nemaweaver-opc.h ../nemaweaver-binutils/opcodes/nemaweaver-opcm.h

    parser = argparse.ArgumentParser(description='Generate binutils from a nemaisa ascii table.')
    parser.add_argument('isa', nargs="?", help="The isa ascii table filename.", type=file, default=DEFAULT_ISA)
    parser.add_argument('opc', nargs="?", help="The isa ascii table filename.", type=file, default=DEFAULT_OPC)
    parser.add_argument('opcm', nargs="?", help="The isa ascii table filename.", type=file, default=DEFAULT_OPCM)

    parser.parse_args(argv)

    isa = InstructionSet(parser.isa)
    isa.opcode_array(parser.opc, parse.opcm)
