import os
import unittest
from pyrametros import parse_file
from re import match

from binutils_gen.opcode import NemaWeaverOpcode, check_duplicates
from binutils_gen.isa import InstructionSet
from binutils_gen.test.config import *

RESOURCE_DIR = "binutils_gen/test"

def resource(fname, resource_dir=RESOURCE_DIR):
    return os.path.join(resource_dir, fname)

ISA_FILE = resource("Nema_ISA.test.txt")

OPC_FILE = resource("nemaweaver-opc.h")
OPCM_FILE = resource("nemaweaver-opcm.h")

OPC_PROTO_FILE = resource("nemaweaver-opc.proto.h")
OPCM_PROTO_FILE = resource("nemaweaver-opcm.proto.h")

OPCODE_ARRAY_FILE = resource("opcode_array.h")
OPCODE_ARRAY_GEN_FILE = resource("opcode_array.gen.h") # Generated array of opcodes

IMM_CONSTANT_STR = "#define ARG_TYPE_IMM 0x"
IMM_CHECK_STR = "#define IMM_TYPE(t) ((t) == ARG_TYPE_IMM)"
IMM_GROUP_STR = "#define IMMEDIATE_TYPE(t) (IMM_TYPE(t) || UIMM_TYPE(t))"
IMM_ARG_GROUP_STR = "#define IMMEDIATE_ARG(arg_i, opcode) (IMMEDIATE_TYPE( OP_BREAD5((arg_i), (opcode)->arg_type) ))"

SLL_OPCODE_STR = '{"sll", OP_BUILD5(5, 5, 5, 0, 0), OP_BUILD5(11, 16, 6, 0, 0), OP_BUILD5(ARG_TYPE_REG, ARG_TYPE_REG, ARG_TYPE_IMM, 0, 0), INST_NO_OFFSET, 0, 2, 0x0, 0xffe0003f, nwop_sll, anyware_inst},'

class TestBinutils(unittest.TestCase):
    """ Test the binutils package.
    """

    def setUp(self, arg_types=ARG_TYPES):
        """ Open files and rad stuff.
	"""
        self.opcodes = [NemaWeaverOpcode(r, arg_types) for r in parse_file(ISA_FILE)]
        self.opcodes = [i for i in self.opcodes if i.valid]
        check_duplicates(self.opcodes)

        self.isa = None

    def test_opcodes(self, opcode_array_file=OPCODE_ARRAY_FILE, opcode_array_gen_file=OPCODE_ARRAY_GEN_FILE):
        """ Test the opcode array generation.
        """
        opc_array = ""
        for o in self.opcodes:
            opc_array += str(o) + '\n'

        with open(opcode_array_gen_file, "w") as gf:
            gf.write(opc_array)

        with open(opcode_array_file, 'r') as f:
            self.assertEquals(opc_array, f.read())

    def test_macros(self, isa_file=ISA_FILE):
        self.isa = InstructionSet(isa_file=isa_file)

        self.assertIn(IMM_CONSTANT_STR, "\n".join([i for i in self.isa.types_manager.type_constant_macros()]))
        self.assertIn(IMM_CHECK_STR, "\n".join([i for i in self.isa.types_manager.type_check_macros()]))
        self.assertIn(IMM_GROUP_STR, "\n".join([i for i in self.isa.types_manager.type_group_macros()]))
        self.assertIn(IMM_ARG_GROUP_STR, "\n".join([i for i in self.isa.types_manager.argument_group_macros()]))

    def test_prefixes(self, isa_file=ISA_FILE):
        self.isa = InstructionSet(isa_file=isa_file)

        self.assertIn("if (REG_TYPE(t))\n\treturn reg_prefix;", "\n".join([i for i in self.isa.types_manager.prefix_selector_code()]))
        self.assertIn("char reg_prefix __attribute__ ((unused)) = \"r\";", "\n".join([i for i in self.isa.types_manager.prefix_variables()]))

    def tearDown(self, opcode_array_gen_file=OPCODE_ARRAY_GEN_FILE):
        """Remove everything from files."""

        open(opcode_array_gen_file, 'w').write("")

        if self.isa is not None:
            self.isa.clean_all()


if __name__ == "__main__":
    unittest.main()
