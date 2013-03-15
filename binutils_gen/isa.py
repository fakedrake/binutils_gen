from pyrametros import CFile, parse_file

from opcode import NemaWeaverOpcode, check_duplicates

class InstructionSet(object):
    """ Container for the opcodes.
    """

    def __init__(self, opcodes=[], isa_file=None):
        """ You may provide raw opcodes and/or a filename for the isa.
	"""

        if opcodes:
            self.opcodes = opcodes
        else:
            self.opcodes = []

        self.isa_file = isa_file

        if isa_file is not None:
            self.opcodes += [NemaWeaverOpcode(r) for r in parse_file(isa_file)]

        self.opcodes = [i for i in self.opcodes if i.valid]

        check_duplicates(self.opcodes)

        self.invalid_opcode = [o for o in self.opcodes if o.name == "invalid"][0]

    def opcode_array(self, opcode_file, names_file, opcode_tag="opcodes", names_tag="opcode names", invalid_tag="invalid opcode"):
        """Create an opcode array and dump into the header file.

        """
        self._opc_fill(names_file, names_tag, representation=lambda o:o.vname() + ",\n")
        self._string_fill("#define INVALID_INST %s\n" % self.invalid_opcode.bit_seq, opcode_file, invalid_tag)
        return self._opc_fill(opcode_file, opcode_tag)


    def _string_fill(self, string, filename, tag):
        """Fill the tags with a specific string."""
        cf = CFile(filename, tag)
        cf.push_line(string)
        cf.flush()

    def _opc_fill(self, filename, tag, representation=lambda o:str(o) + '\n'):
        """Fill the name undet tag with the string function tha accepts an
        opcode.

        """
        cf = CFile(filename, tag)

        for o in self.opcodes:
            cf.push_line(representation(o))

        cf.flush()

    def clean_all(self, opcode_file, names_file, opcode_tag="opcodes", names_tag="opcode names", invalid_tag="invalid opcode"):
        """Clear the contents of all files"""
        self.clean_tag(names_file, names_tag)
        self.clean_tag(opcode_file, invalid_tag)
        self.clean_tag(opcode_file, opcode_tag)

    def clean_tag(self, filename, tag):
        self._string_fill("\n", filename, tag)
