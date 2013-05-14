from sys import argv
import argparse
import os

from binutils_gen.config import DEFAULT_DIS, DEFAULT_OPCM, DEFAULT_OPC, DEFAULT_ISA, DEFAULT_TRANS, BINUTILS_GEN_DESCRIPTION
from binutils_gen.isa import InstructionSet
from binutils_gen.opcode import NemaWeaverOpcode, check_duplicates


def main():
    # You may want to run
    # python binutils.py Nema_ISA.txt ../nemaweaver-binutils/opcodes/nemaweaver-opc.h ../nemaweaver-binutils/opcodes/nemaweaver-opcm.h

    parser = argparse.ArgumentParser(description=BINUTILS_GEN_DESCRIPTION)
    parser.add_argument('isa', nargs="?", help="The isa ascii table filename. Default is '%s'" % DEFAULT_ISA, default=DEFAULT_ISA)
    parser.add_argument('opc', nargs="?", help="The opcode header filename. Default is '%s'" % DEFAULT_OPC, default=DEFAULT_OPC)
    parser.add_argument('opcm', nargs="?", help="The isa opcode names filename. Default is '%s'" % DEFAULT_OPCM, default=DEFAULT_OPCM)
    parser.add_argument('dis', nargs="?", help="The disassembler filename. Default is '%s'" % DEFAULT_DIS, default=DEFAULT_DIS)
    parser.add_argument('trans', nargs="?", help="The filename where the opcode transformations live. That would be in the JUMP column an arg of the form rl:<opc name>. Default is '%s'" % DEFAULT_TRANS, default=DEFAULT_TRANS)


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
