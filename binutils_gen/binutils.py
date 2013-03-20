import os
import argparse
from sys import argv

from config import DEFAULT_NEMA_ROOT
from binutils_gen.opcode import NemaWeaverOpcode, check_duplicates
from binutils_gen.isa import InstructionSet

def nema_root(rel_fname, root=DEFAULT_NEMA_ROOT):
    """ Nemaweaver root.
    """
    env_root = os.getenv('NEMA_ROOT')

    if env_root is not None:
        root = env_root

    return os.path.abspath(os.path.join(root, rel_fname))


DEFAULT_OPC = nema_root("nemaweaver-binutils/opcodes/nemaweaver-opc.h")
DEFAULT_OPCM = nema_root("nemaweaver-binutils/opcodes/nemaweaver-opcm.h")
DEFAULT_ISA = nema_root("NemaSpec/Nema_ISA.txt")


def main():
    # You may want to run
    # python binutils.py Nema_ISA.txt ../nemaweaver-binutils/opcodes/nemaweaver-opc.h ../nemaweaver-binutils/opcodes/nemaweaver-opcm.h

    parser = argparse.ArgumentParser(description='Generate binutils from a nemaisa ascii table.')
    parser.add_argument('isa', nargs="?", help="The isa ascii table filename.", default=DEFAULT_ISA)
    parser.add_argument('opc', nargs="?", help="The opcode header filename.", default=DEFAULT_OPC)
    parser.add_argument('opcm', nargs="?", help="The isa opcode names filename.", default=DEFAULT_OPCM)

    parser.add_argument('--clean', '-c', help="The isa opcode names filename.", action='store_true')

    args = parser.parse_args(argv[1:])

    print "ISA Table: %s" % args.isa
    print "Opcode header: %s" % args.opc
    print "Ocode names header: %s" % args.opcm

    isa = InstructionSet(isa_file=args.isa)

    if args.clean == True:
        print "Clearing everything I have created..."
        isa.clean_all(args.opc, args.opcm)
    else:
        print "Creating opcodes..."
        isa.opcode_array(args.opc, args.opcm)
        print "Creating types..."
        isa.types_array(args.opc)
