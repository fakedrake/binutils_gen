from functools import partial

from pyrametros import CFile, parse_file

from opcode import NemaWeaverOpcode, check_duplicates
from argument_types_manager import ArgumentTypeManager
from config import *
from binutils_gen.transform import transforms

class InstructionSet(object):
    """ Container for the opcodes.
    """

    def __init__(self, opcodes=[], isa_file=None, arg_types=ARG_TYPES, arg_type_groups=ARG_TYPE_GROUPS):
        """ You may provide raw opcodes and/or a filename for the isa.
	"""
        self.arg_type_groups = arg_type_groups
        self.arg_types = arg_types

        if opcodes:
            self.opcodes = opcodes
        else:
            self.opcodes = []

        self.isa_file = isa_file

        if isa_file is not None:
            self.opcodes += [NemaWeaverOpcode(r, arg_types) for r in parse_file(isa_file)]

        self.opcodes = [i for i in self.opcodes if i.valid]

        check_duplicates(self.opcodes)

        self.invalid_opcode = [o for o in self.opcodes if o.name == "invalid"][0]

        self.types_manager = ArgumentTypeManager(self.arg_types, HARDCODED_TYPES, self.arg_type_groups)
        self._to_clean = []

    def opcode_array(self, opcode_file, names_file, opcode_tag=OPCODES_TAG, names_tag=OPCODE_NAMES_TAG, invalid_tag=INVALID_TAG):
        """Create an opcode array and dump into the header file.

        """
        self._opc_fill(names_file, names_tag, representation=lambda o:o.vname() + ",\n")
        self._string_fill("#define INVALID_INST %s\n" % self.invalid_opcode.bit_seq, opcode_file, invalid_tag)
        return self._opc_fill(opcode_file, opcode_tag)

    def types_array(self, filename, dis_filename, type_constant_tag=TYPE_CONSTANT_TAG, type_checks_tag=TYPE_CHECKS_TAG, type_groups_tag=TYPE_GROUPS_TAG, argument_groups_tag=ARGUMENT_GROUPS_TAG, type_prefixes_tag=TYPE_PREFIXES_TAG, type_prefixes_check_tag=TYPE_PREFIXES_CHECK_TAG):
        """Fill in the types and types' groups"""

        self._strings_fill(self.types_manager.type_constant_macros, filename, type_constant_tag)
        self._strings_fill(self.types_manager.type_check_macros, filename, type_checks_tag)
        self._strings_fill(self.types_manager.type_group_macros, filename, type_groups_tag)
        self._strings_fill(self.types_manager.argument_group_macros, filename, argument_groups_tag)

        self._strings_fill(self.types_manager.prefix_variables, filename, type_prefixes_tag)
        self._strings_fill(self.types_manager.prefix_selector_code, dis_filename, type_prefixes_check_tag)

    def opcode_transforms_array(self, filename, opcode_map_tag=OPCODE_MAP_TAG):
        self._strings_fill(partial(transforms, self.opcodes), filename, opcode_map_tag)

    def _strings_fill(self, string_gen, filename, tag):
        """Fill up the tag with a list of strings.
        """

        self._to_clean.append((filename, tag))

        cf = CFile(filename, tag)
        cf.push_lines(["%s\n" % s for s in string_gen()])
        cf.flush()

    def _string_fill(self, string, filename, tag, clean=False):
        """Fill the tags with a specific string."""

        if not clean:
            self._to_clean.append((filename, tag))

        cf = CFile(filename, tag)
        cf.push_line(string)
        cf.flush()

    def _opc_fill(self, filename, tag, representation=lambda o:str(o) + '\n'):
        """Fill the name under tag with the string function that accepts an
        opcode.

        """

        self._to_clean.append((filename, tag))

        cf = CFile(filename, tag)

        for o in self.opcodes:
            cf.push_line(representation(o))

        cf.flush()
        return cf.filling_string()


    def clean_all(self):
        """Clear the contents of all files"""
        for i in self._to_clean:
            self.clean_tag(i)

    def clean_tag(self, (filename, tag)):
        self._string_fill("\n", filename, tag, clean=True)
