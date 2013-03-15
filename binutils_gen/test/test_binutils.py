import os
import unittest
from pyrametros import parse_file

from binutils_gen.opcode import NemaWeaverOpcode, check_duplicates
from binutils_gen.isa import InstructionSet

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

class TestBinutils(unittest.TestCase):
    """ Test the binutils package.
    """

    def setUp(self):
        """ Open files and rad stuff.
	"""
        self.opcodes = [NemaWeaverOpcode(r) for r in parse_file(ISA_FILE)]
        self.opcodes = [i for i in self.opcodes if i.valid]
        check_duplicates(self.opcodes)

    def test_argument_types(self):
        """Test that the argument types are calculated correctly."""


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

    def test_generation(self, isa_file=ISA_FILE, opc_file=OPC_FILE, opcm_file=OPCM_FILE, opc_proto=OPC_PROTO_FILE, opcm_proto=OPCM_PROTO_FILE):
        """ Test the entire process"""

        isa = InstructionSet(isa_file=isa_file)
        isa.opcode_array(opc_file, opcm_file)

    def tearDown(self, isa_file=ISA_FILE, opc_file=OPC_FILE, opcm_file=OPCM_FILE, opcode_array_gen_file=OPCODE_ARRAY_GEN_FILE):
        """Remove everything from files."""

        open(opcode_array_gen_file, 'w').write("")

        isa = InstructionSet(isa_file=isa_file)
        isa.clean_all(opc_file, opcm_file)


if __name__ == "__main__":
    unittest.main()
