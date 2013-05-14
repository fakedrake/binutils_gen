#!/usr/bin/python
import argparse
import re
import sys
import os

from pyrametros import CFile

from binutils_gen.config import DEFAULT_GAS_HEADER, DEFAULT_LD_MAP, LIBSYMBOL_DESCRIPTION

class Symbol(object):
    """A symbol that knows it's place.

    Set string_template to edit the string that symbol will be
    exported to. It will be formatted with attributes 'name' and
    'value'

    """

    def __init__(self, name, value, object_file, string_template="%(name)ss = %(value)s;"):
        """ Given a file offset and a global offset.
	"""
        self.name = name
        self.value = value
        self.object_file = object_file
        self.string_template = string_template

    def __int__(self):
        return int(self.value, 16) + self.object_file.offset

    def __str__(self):
        return self.string_template % dict(name=self.name, value=hex(int(self)))


class ObjectFile(object):
    """ A container for symbols.

    Get a list of the symbols from symbols attribute.
    """

    def __init__(self, filename, local_offset, global_offset=0, nm_executable="nm", nm_arguments="-g"):
        """Provide the filename of an elf object and the offset of the object
        in memory.

        """
        self.filename = filename
        self.local_offset = local_offset
        self.global_offset = global_offset

        lines = os.popen(" ".join([nm_executable, nm_arguments, filename])).readlines()
        symbols = [parse_symbol(l.strip(), self) for l in lines]
        self.symbols = [s for s in symbols if s is not None]

    def format_symbols(self, format_str):
        """Set the formatting of the symbols."""
        for s in self.symbols:
            s.string_template = format_str

    @property
    def offset(self):
        return self.local_offset + self.global_offset

    @property
    def size(self):
        """Return the size of the object file in memory"""
        return os.stat(self.filename).st_size

    def __str__(self):
        return "\n".join([str(s) for s in self.symbols]) + "\n"


def aligned_objects(obj_names_list, offset=0, nm_executable="nm", nm_arguments="-g"):
    """Generate object file objects aligned to offset.
    """

    for n in obj_names_list:
        o = ObjectFile(n, offset, nm_executable=nm_executable, nm_arguments=nm_arguments)
        yield o

        offset += o.size

def symbol_map(obj_names_list, offset=0, nm_executable="nm", nm_arguments="-g"):
    """Given a list of obkect filenames return a list of their
    symbols. This uses the default formatting for symbol
    representation. Please refer to aligned_objects to change that.

    """

    return "\n".join([str(f) for f in aligned_objects(obj_names_list, offset, nm_executable, nm_arguments)])

def parse_symbol(sym, obj_file):
    """ Given a sting from the nm command that represents a symbol, return
    a Symbol object.
    """

    arr = sym.split(" ")
    if len(arr) == 3 and re.match("[A-Z]", arr[1]):
        return Symbol(arr[2], arr[0], obj_file)

    return None

def main():
    """"The main entry point for symbol parsing."""

    parser = argparse.ArgumentParser(description=LIBSYMBOL_DESCRIPTION)
    parser.add_argument('objs', metavar="OBJS",  nargs="+", help="Object files in the order they are placed to be placed in memory.")
    parser.add_argument('--offset', '-o', help="Object offset, by default 0", type=int, default=0)
    parser.add_argument('--nm', '-n', help="nm executable. By default 'nm'", default='nm')
    parser.add_argument('--gas-header', '-g',
                        help="The header file to insert the names of the symbols which when gas \
encounters will change the jump opcode to absolute jump. The tag used \
is 'external symbols'. By default this is '%s'" % DEFAULT_GAS_HEADER,
                        default=DEFAULT_GAS_HEADER)
    parser.add_argument('--no-gas', help="Dont touch gas headers at all.", action='store_true')

    parser.add_argument('--ld-map', '-l',
                            help="Linker symbol map file. This file is to be passed to the linker when \
linking a NemaWeaver executable using the -R option. Default is '%s'." % DEFAULT_LD_MAP,
                            default=DEFAULT_LD_MAP)
    parser.add_argument('-c', '--clean', help="Clear symbols from gas header file. This will be the only action taken.", action='store_true')

    args = parser.parse_args(sys.argv[1:])

    if args.clean == True:
        print "Clearing everything in %s..." % args.gas_header
        cf = CFile(args.gas_header, "external symbols")
        cf.push_line("\n")
        cf.flush()
        return

    with open(args.ld_map, 'w') as ld_map_file:
        print "Writing ld symbol map to file '%s'." % args.ld_map
        ld_map_file.write( symbol_map(args.objs, offset=args.offset, nm_executable=args.nm) )


    if not args.no_gas:
        print "Writing the symbol names for cfile in '%s'." % args.gas_header

        cf = CFile(args.gas_header, "external symbols")
        for o in aligned_objects(args.objs, offset=args.offset, nm_executable=args.nm):
            o.format_symbols("\"%(name)s\", \\")
            cf.push_line(str(o))
            cf.flush()


if __name__ == "__main__":
    main()
