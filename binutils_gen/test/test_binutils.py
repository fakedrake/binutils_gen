import os
import unittest
from pyrametros import parse_file

from binutils_gen.opcode import NemaWeaverOpcode, check_duplicates

RESOURCE_DIR = "binutils_gen/test"

def resource(fname, resource_dir=RESOURCE_DIR):
    return os.path.join(resource_dir, fname)

ISA_FILE = resource("Nema_ISA.test.txt")
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

        with open(opcode_array_file) as f:
            self.assertEquals(opc_array, f.read())


if __name__ == "__main__":
    unittest.main()
