import os
import argparse
from sys import argv

from binutils_gen.config import DEFAULT_NEMA_ROOT
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
DEFAULT_DIS = nema_root("nemaweaver-binutils/opcodes/nemaweaver-dis.c")
DEFAULT_TRANS = nema_root("nemaweaver-binutils/gas/config/tc-nemaweaver.h")


def main():
    # You may want to run
    # python binutils.py Nema_ISA.txt ../nemaweaver-binutils/opcodes/nemaweaver-opc.h ../nemaweaver-binutils/opcodes/nemaweaver-opcm.h

    parser = argparse.ArgumentParser(description='Generate binutils from a nemaisa ascii table. The root directory of  the nema project is given by the NEMA_ROOT variable, otherwise I will assume you are in NemaSpec/')
    parser.add_argument('isa', nargs="?", help="The isa ascii table filename.", default=DEFAULT_ISA)
    parser.add_argument('opc', nargs="?", help="The opcode header filename.", default=DEFAULT_OPC)
    parser.add_argument('opcm', nargs="?", help="The isa opcode names filename.", default=DEFAULT_OPCM)
    parser.add_argument('dis', nargs="?", help="The disassembler filename.", default=DEFAULT_DIS)
    parser.add_argument('trans', nargs="?", help="The filename where the opcode transformations live. That would be in the JUMP column an arg of the form rl:<opc name>", default=DEFAULT_TRANS)


    parser.add_argument('-c', '--clean', help="Clear everything binutils_gen is responsible for generating.", action='store_true')

    args = parser.parse_args(argv[1:])

    print "ISA Table: %s" % args.isa
    print "Opcode header: %s" % args.opc
    print "Ocode names header: %s" % args.opcm
    print "Disassembler source: %s" % args.dis
    print "Transfomations file: %s" % args.trans

    isa = InstructionSet(isa_file=args.isa)

    if args.clean == True:
        print "Clearing everything I have created..."
        isa.clean_all(args.opc, args.opcm)
    else:
        print "Creating opcodes..."
        isa.opcode_array(args.opc, args.opcm)
        print "Creating types..."
        isa.types_array(args.opc, args.dis)
        print "Creating transforms..."
        isa.opcode_transforms_array(args.trans)
