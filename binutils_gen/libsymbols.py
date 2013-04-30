#!/usr/bin/python
import argparse
import re
import sys
import os

from pyrametros import CFile

SYMBOL_REGEX = r"[0-9]+ [a-zA-Z] [^\s]+"
TC_NEMAWEAVER_H = "../../nemaweaver-binutils/gas/config/tc-nemaweaver.h"

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
    return "\n".join([str(f) for f in aligned_objects(obj_names_list, offset, nm_executable, nm_arguments)])

def parse_symbol(sym, obj_file):
    arr = sym.split(" ")
    if len(arr) == 3 and re.match("[A-Z]", arr[1]):
        return Symbol(arr[2], arr[0], obj_file)

    return None

def main():
    """"The main entry point for symbol parsing."""
    parser = argparse.ArgumentParser(description='Get a list of symbols and their offsets in memory given the files.')
    parser.add_argument('objs', metavar="OBJ",  nargs="+", help="Object files in the order they are placed in memory.")
    parser.add_argument('--offset', '-o', help="Object offset", type=int, default=0)
    parser.add_argument('--nm', '-n', help="nm executable", default='nm')
    parser.add_argument('--exeternal', '-e',
                        help="The header file to insert the names of the symbols. The tag used is
                        'external symbols'",
                        default=TC_NEMAWEAVER_H)
    parser.add_argument('--no-external', help="Dont do the external sybol part.", action='store_true')


    args = parser.parse_args(sys.argv[1:])

    print symbol_map(args.objs, offset=args.offset, nm_executable=args.nm)

    if not args.no_external:
        print "Now the symbol names for cfile"

        cf = CFile(args.external, "external symbols")
        for o in aligned_objects(args.objs, offset=args.offset, nm_executable=args.nm):
            o.format_symbols("\"%(name)s\", \\")
            cf.push_line(str(o))
            print cf.filling_string()
            cf.flush()


if __name__ == "__main__":
    main()
